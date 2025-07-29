import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "/bin/bash",
  args: ["-c", "clojure -X:mcp :port 7888"]
});

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0"
  }
);

await client.connect(transport);

// List prompts
const prompts = await client.listPrompts();

// Get a prompt : 没有这个提示词："example-prompt",
//const prompt = await client.getPrompt({
//  name: "example-prompt",
//  arguments: {
//    arg1: "value"
//  }
//});

// List resources
const resources = await client.listResources();

// Read a resource
//const resource = await client.readResource({
//  uri: "file:///Users/clojure/Desktop/web-mcp-client/docs.md"
//});

// Call a tool
const result = await client.callTool({
  name: "read_file",
  arguments: {
    path: "test.md" // => /Users/clojure/Desktop/clojure-mcp
  }
});

console.log(result);
//
//@ node mcp_client_v0.js
//(node:23900) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/clojure/Desktop/web-mcp-client/mcp_client_v0.js is not specified and it doesn't parse as CommonJS.
//Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
//To eliminate this warning, add "type": "module" to /Users/clojure/Desktop/web-mcp-client/package.json.
//(Use `node --trace-warnings ...` to show where the warning was created)
//{
//  content: [
//    {
//      type: 'text',
//      text: '### /Users/clojure/Desktop/clojure-mcp/test.md\n' +
//        '```md\n' +
//        'Hi, MCP client\n' +
//        '```'
//    }
//  ],
//  isError: false
//}
//
