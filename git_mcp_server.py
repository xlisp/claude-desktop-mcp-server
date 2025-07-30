import os
import subprocess
from typing import Any, Optional
import asyncio
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("git-operations")

async def run_git_command(repo_path: str, command: list[str]) -> tuple[str, str]:
    """Run a git command in the specified repository directory."""
    if not os.path.exists(repo_path):
        return "", f"Repository path does not exist: {repo_path}"
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "", f"Not a git repository: {repo_path}"
    
    try:
        # Run git command
        process = await asyncio.create_subprocess_exec(
            'git', *command,
            cwd=repo_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, 'LC_ALL': 'C.UTF-8'}
        )
        stdout, stderr = await process.communicate()
        
        return stdout.decode('utf-8', errors='replace'), stderr.decode('utf-8', errors='replace')
    except Exception as e:
        return "", f"Error running git command: {str(e)}"

def format_commit_info(commit_line: str) -> str:
    """Format a single commit line into readable format."""
    parts = commit_line.strip().split('|', 4)
    if len(parts) >= 4:
        hash_short = parts[0]
        date = parts[1]
        author = parts[2]
        message = parts[3]
        return f"[{hash_short}] {date} - {author}\n  {message}"
    return commit_line

@mcp.tool()
async def search_file_history(repo_path: str, filename: str, limit: int = 10) -> str:
    """Search when a specific file was first introduced and its history.
    
    Args:
        repo_path: Path to the git repository
        filename: Name or path of the file to search for
        limit: Maximum number of commits to show (default: 10)
    """
    # Search for commits that modified the file
    stdout, stderr = await run_git_command(
        repo_path, 
        ['log', '--oneline', '--follow', f'--max-count={limit}', '--', filename]
    )
    
    if stderr:
        return f"Error: {stderr}"
    
    if not stdout.strip():
        return f"No commits found for file: {filename}"
    
    # Get detailed information about the file's history
    detailed_stdout, _ = await run_git_command(
        repo_path,
        ['log', '--follow', f'--max-count={limit}', 
         '--pretty=format:%h|%ai|%an|%s', '--', filename]
    )
    
    lines = detailed_stdout.strip().split('\n')
    formatted_commits = [format_commit_info(line) for line in lines if line.strip()]
    
    result = f"History of file '{filename}':\n\n"
    result += "\n\n".join(formatted_commits)
    
    # Try to find when the file was first added
    first_commit_stdout, _ = await run_git_command(
        repo_path,
        ['log', '--follow', '--diff-filter=A', '--pretty=format:%h|%ai|%an|%s', '--', filename]
    )
    
    if first_commit_stdout.strip():
        first_line = first_commit_stdout.strip().split('\n')[0]
        first_commit = format_commit_info(first_line)
        result += f"\n\n🎯 File first introduced in:\n{first_commit}"
    
    return result

@mcp.tool()
async def search_commits_by_message(repo_path: str, search_term: str, limit: int = 10) -> str:
    """Search commits by commit message content.
    
    Args:
        repo_path: Path to the git repository
        search_term: Text to search for in commit messages
        limit: Maximum number of commits to show (default: 10)
    """
    stdout, stderr = await run_git_command(
        repo_path,
        ['log', f'--grep={search_term}', f'--max-count={limit}', 
         '--pretty=format:%h|%ai|%an|%s', '--all']
    )
    
    if stderr:
        return f"Error: {stderr}"
    
    if not stdout.strip():
        return f"No commits found containing: {search_term}"
    
    lines = stdout.strip().split('\n')
    formatted_commits = [format_commit_info(line) for line in lines if line.strip()]
    
    result = f"Commits containing '{search_term}':\n\n"
    result += "\n\n".join(formatted_commits)
    
    return result

@mcp.tool()
async def find_branches_with_feature(repo_path: str, search_term: str) -> str:
    """Find branches that contain commits with specific features or keywords.
    
    Args:
        repo_path: Path to the git repository
        search_term: Feature or keyword to search for
    """
    # First find commits with the search term
    stdout, stderr = await run_git_command(
        repo_path,
        ['log', f'--grep={search_term}', '--pretty=format:%H', '--all']
    )
    
    if stderr:
        return f"Error: {stderr}"
    
    if not stdout.strip():
        return f"No commits found containing: {search_term}"
    
    commit_hashes = stdout.strip().split('\n')
    branch_info = {}
    
    # For each commit, find which branches contain it
    for commit_hash in commit_hashes[:5]:  # Limit to first 5 commits
        branch_stdout, _ = await run_git_command(
            repo_path,
            ['branch', '-a', '--contains', commit_hash]
        )
        
        if branch_stdout:
            branches = [b.strip().lstrip('* ') for b in branch_stdout.split('\n') if b.strip()]
            
            # Get commit info
            commit_info_stdout, _ = await run_git_command(
                repo_path,
                ['show', '--no-patch', '--pretty=format:%h|%ai|%an|%s', commit_hash]
            )
            
            if commit_info_stdout:
                branch_info[commit_hash] = {
                    'commit_info': format_commit_info(commit_info_stdout),
                    'branches': branches
                }
    
    if not branch_info:
        return f"No branch information found for commits containing: {search_term}"
    
    result = f"Branches containing commits with '{search_term}':\n\n"
    
    for commit_hash, info in branch_info.items():
        result += f"📍 {info['commit_info']}\n"
        result += f"   Found in branches: {', '.join(info['branches'])}\n\n"
    
    return result

@mcp.tool()
async def get_commit_info(repo_path: str, commit_hash: str) -> str:
    """Get detailed information about a specific commit.
    
    Args:
        repo_path: Path to the git repository
        commit_hash: Hash of the commit to examine
    """
    # Get commit details
    stdout, stderr = await run_git_command(
        repo_path,
        ['show', '--stat', '--pretty=format:%H%n%ai%n%an <%ae>%n%s%n%n%b', commit_hash]
    )
    
    if stderr:
        return f"Error: {stderr}"
    
    if not stdout.strip():
        return f"Commit not found: {commit_hash}"
    
    # Get files changed in this commit
    files_stdout, _ = await run_git_command(
        repo_path,
        ['show', '--name-status', '--pretty=format:', commit_hash]
    )
    
    result = f"📋 Commit Details:\n\n{stdout}"
    
    if files_stdout.strip():
        result += f"\n\n📁 Files changed:\n{files_stdout}"
    
    return result

@mcp.tool()
async def find_commit_introducing_text(repo_path: str, text: str, file_path: str = "") -> str:
    """Find the commit that introduced specific text or code.
    
    Args:
        repo_path: Path to the git repository
        text: Text or code to search for
        file_path: Optional specific file to search in (empty for all files)
    """
    command = ['log', '-S', text, '--oneline', '--all']
    if file_path:
        command.extend(['--', file_path])
    
    stdout, stderr = await run_git_command(repo_path, command)
    
    if stderr:
        return f"Error: {stderr}"
    
    if not stdout.strip():
        search_scope = f"in file '{file_path}'" if file_path else "in repository"
        return f"No commits found that introduced text '{text}' {search_scope}"
    
    # Get detailed info for the commits
    commit_hashes = [line.split()[0] for line in stdout.strip().split('\n')]
    
    result = f"Commits that introduced text '{text}':\n\n"
    
    for commit_hash in commit_hashes[:5]:  # Limit to first 5 commits
        detail_stdout, _ = await run_git_command(
            repo_path,
            ['show', '--no-patch', '--pretty=format:%h|%ai|%an|%s', commit_hash]
        )
        
        if detail_stdout:
            result += format_commit_info(detail_stdout) + "\n\n"
    
    return result

@mcp.tool()
async def get_repository_summary(repo_path: str) -> str:
    """Get a summary of the repository including branches, recent commits, and basic stats.
    
    Args:
        repo_path: Path to the git repository
    """
    # Get current branch
    current_branch_stdout, _ = await run_git_command(repo_path, ['branch', '--show-current'])
    current_branch = current_branch_stdout.strip()
    
    # Get all branches
    branches_stdout, _ = await run_git_command(repo_path, ['branch', '-a'])
    
    # Get recent commits
    recent_commits_stdout, _ = await run_git_command(
        repo_path, 
        ['log', '--oneline', '--max-count=5', '--pretty=format:%h|%ai|%an|%s']
    )
    
    # Get repository stats
    total_commits_stdout, _ = await run_git_command(repo_path, ['rev-list', '--count', 'HEAD'])
    
    # Get contributors
    contributors_stdout, _ = await run_git_command(
        repo_path, 
        ['shortlog', '-sn', '--all', '--max-count=10']
    )
    
    result = f"📊 Repository Summary\n"
    result += f"==================\n\n"
    
    result += f"📂 Current Branch: {current_branch}\n\n"
    
    if total_commits_stdout.strip():
        result += f"📈 Total Commits: {total_commits_stdout.strip()}\n\n"
    
    if branches_stdout:
        branch_lines = [b.strip() for b in branches_stdout.split('\n') if b.strip()]
        result += f"🌿 Branches ({len(branch_lines)}):\n"
        for branch in branch_lines[:10]:  # Show first 10 branches
            result += f"  {branch}\n"
        result += "\n"
    
    if recent_commits_stdout:
        result += f"📝 Recent Commits:\n"
        lines = recent_commits_stdout.strip().split('\n')
        for line in lines:
            if line.strip():
                result += format_commit_info(line) + "\n"
        result += "\n"
    
    if contributors_stdout:
        result += f"👥 Top Contributors:\n"
        result += contributors_stdout + "\n"
    
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

