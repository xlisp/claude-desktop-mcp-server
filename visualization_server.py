import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import networkx as nx
from typing import Any, List, Optional, Union
import json
import base64
import io
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("visualization")

def encode_plot_to_base64() -> str:
    """将matplotlib图形编码为base64字符串"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()  # 关闭图形释放内存
    return image_base64

@mcp.tool()
async def create_relationship_graph(
    nodes: List[str], 
    edges: List[List[str]], 
    title: str = "关系图",
    node_size: int = 1000,
    font_size: int = 12
) -> str:
    """创建节点关系图
    
    Args:
        nodes: 节点列表，例如 ["A", "B", "C", "D"]
        edges: 边的列表，例如 [["A", "B"], ["B", "C"], ["A", "C"]]
        title: 图表标题
        node_size: 节点大小
        font_size: 字体大小
    
    Returns:
        base64编码的图像字符串
    """
    try:
        # 创建有向图
        G = nx.DiGraph()
        
        # 添加节点
        G.add_nodes_from(nodes)
        
        # 添加边
        for edge in edges:
            if len(edge) >= 2:
                G.add_edge(edge[0], edge[1])
        
        # 创建图形
        plt.figure(figsize=(10, 8))
        
        # 使用spring布局
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=node_size, alpha=0.8)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, arrowstyle='->')
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建关系图时出错: {str(e)}"

@mcp.tool()
async def create_scatter_plot(
    x_data: List[float],
    y_data: List[float],
    labels: Optional[List[str]] = None,
    colors: Optional[List[str]] = None,
    title: str = "散点图",
    x_label: str = "X轴",
    y_label: str = "Y轴",
    size: int = 50
) -> str:
    """创建散点图
    
    Args:
        x_data: X轴数据
        y_data: Y轴数据
        labels: 数据点标签（可选）
        colors: 数据点颜色（可选）
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
        size: 点的大小
    
    Returns:
        base64编码的图像字符串
    """
    try:
        plt.figure(figsize=(10, 8))
        
        # 如果没有提供颜色，使用默认颜色
        if colors is None:
            colors = ['blue'] * len(x_data)
        
        # 创建散点图
        scatter = plt.scatter(x_data, y_data, c=colors, s=size, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # 添加标签（如果提供）
        if labels:
            for i, label in enumerate(labels):
                if i < len(x_data) and i < len(y_data):
                    plt.annotate(label, (x_data[i], y_data[i]), 
                               xytext=(5, 5), textcoords='offset points',
                               fontsize=10, alpha=0.8)
        
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建散点图时出错: {str(e)}"

@mcp.tool()
async def create_3d_plot(
    x_data: List[float],
    y_data: List[float],
    z_data: List[float],
    plot_type: str = "scatter",
    title: str = "3D图",
    x_label: str = "X轴",
    y_label: str = "Y轴",
    z_label: str = "Z轴"
) -> str:
    """创建3D图
    
    Args:
        x_data: X轴数据
        y_data: Y轴数据
        z_data: Z轴数据
        plot_type: 图表类型 ("scatter", "surface", "wireframe")
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
        z_label: Z轴标签
    
    Returns:
        base64编码的图像字符串
    """
    try:
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        if plot_type == "scatter":
            ax.scatter(x_data, y_data, z_data, c=z_data, cmap='viridis', s=50)
            
        elif plot_type == "surface":
            # 为表面图创建网格
            x_array = np.array(x_data)
            y_array = np.array(y_data)
            z_array = np.array(z_data)
            
            # 尝试重塑数据为2D网格
            unique_x = sorted(set(x_data))
            unique_y = sorted(set(y_data))
            
            if len(unique_x) * len(unique_y) == len(z_data):
                X = np.array(unique_x)
                Y = np.array(unique_y)
                X, Y = np.meshgrid(X, Y)
                Z = np.array(z_data).reshape(len(unique_y), len(unique_x))
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
            else:
                # 如果无法创建规则网格，回退到散点图
                ax.scatter(x_data, y_data, z_data, c=z_data, cmap='viridis', s=50)
                
        elif plot_type == "wireframe":
            # 类似surface的处理
            unique_x = sorted(set(x_data))
            unique_y = sorted(set(y_data))
            
            if len(unique_x) * len(unique_y) == len(z_data):
                X = np.array(unique_x)
                Y = np.array(unique_y)
                X, Y = np.meshgrid(X, Y)
                Z = np.array(z_data).reshape(len(unique_y), len(unique_x))
                ax.plot_wireframe(X, Y, Z, alpha=0.8)
            else:
                ax.scatter(x_data, y_data, z_data, c=z_data, cmap='viridis', s=50)
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        ax.set_title(title, fontsize=16, fontweight='bold')
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建3D图时出错: {str(e)}"

@mcp.tool()
async def create_classification_plot(
    x_data: List[float],
    y_data: List[float],
    categories: List[str],
    title: str = "分类散点图",
    x_label: str = "特征1",
    y_label: str = "特征2"
) -> str:
    """创建分类散点图
    
    Args:
        x_data: X轴数据
        y_data: Y轴数据
        categories: 分类标签
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
    
    Returns:
        base64编码的图像字符串
    """
    try:
        plt.figure(figsize=(10, 8))
        
        # 获取唯一的分类
        unique_categories = list(set(categories))
        colors = plt.cm.Set1(np.linspace(0, 1, len(unique_categories)))
        
        # 为每个类别绘制散点
        for i, category in enumerate(unique_categories):
            # 找出属于当前类别的数据点
            mask = [cat == category for cat in categories]
            x_cat = [x for x, m in zip(x_data, mask) if m]
            y_cat = [y for y, m in zip(y_data, mask) if m]
            
            plt.scatter(x_cat, y_cat, c=[colors[i]], label=category, 
                       s=60, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建分类图时出错: {str(e)}"

@mcp.tool()
async def create_histogram(
    data: List[float],
    bins: int = 30,
    title: str = "直方图",
    x_label: str = "值",
    y_label: str = "频次"
) -> str:
    """创建直方图
    
    Args:
        data: 数据列表
        bins: 分箱数量
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
    
    Returns:
        base64编码的图像字符串
    """
    try:
        plt.figure(figsize=(10, 6))
        
        plt.hist(data, bins=bins, alpha=0.7, color='skyblue', edgecolor='black', linewidth=0.5)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建直方图时出错: {str(e)}"

@mcp.tool()
async def create_line_plot(
    x_data: List[float],
    y_data: List[float],
    title: str = "折线图",
    x_label: str = "X轴",
    y_label: str = "Y轴",
    line_style: str = "-",
    color: str = "blue"
) -> str:
    """创建折线图
    
    Args:
        x_data: X轴数据
        y_data: Y轴数据
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
        line_style: 线条样式 ("-", "--", "-.", ":")
        color: 线条颜色
    
    Returns:
        base64编码的图像字符串
    """
    try:
        plt.figure(figsize=(10, 6))
        
        plt.plot(x_data, y_data, linestyle=line_style, color=color, linewidth=2, marker='o', markersize=4)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建折线图时出错: {str(e)}"

@mcp.tool()
async def create_heatmap(
    data: List[List[float]],
    x_labels: Optional[List[str]] = None,
    y_labels: Optional[List[str]] = None,
    title: str = "热力图",
    colormap: str = "viridis"
) -> str:
    """创建热力图
    
    Args:
        data: 2D数据矩阵
        x_labels: X轴标签（可选）
        y_labels: Y轴标签（可选）
        title: 图表标题
        colormap: 颜色映射 ("viridis", "plasma", "hot", "cool")
    
    Returns:
        base64编码的图像字符串
    """
    try:
        plt.figure(figsize=(10, 8))
        
        im = plt.imshow(data, cmap=colormap, aspect='auto')
        
        if x_labels:
            plt.xticks(range(len(x_labels)), x_labels, rotation=45, ha='right')
        if y_labels:
            plt.yticks(range(len(y_labels)), y_labels)
            
        plt.colorbar(im, shrink=0.8)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return encode_plot_to_base64()
        
    except Exception as e:
        return f"创建热力图时出错: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

