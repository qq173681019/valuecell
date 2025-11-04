# ValueCell DeepSeek 配置指南

## 概述

由于地区限制无法使用OpenAI API的用户，可以使用DeepSeek作为替代方案。DeepSeek提供与OpenAI兼容的API接口，性能优秀且在更多地区可用。

## 配置步骤

### 1. 获取DeepSeek API密钥

1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册账户并登录
3. 进入API密钥页面：https://platform.deepseek.com/api_keys
4. 创建新的API密钥

### 2. 配置环境变量

#### 方法一：使用提供的模板文件

```bash
# 复制DeepSeek配置模板
cp .env.deepseek.example .env

# 编辑.env文件，添加你的API密钥
# 将 "你的_DEEPSEEK_API_KEY" 替换为实际的API密钥
```

#### 方法二：手动配置

1. 复制原始模板文件：
   ```bash
   cp .env.example .env
   ```

2. 在`.env`文件中添加以下配置：
   ```bash
   # 设置主要提供商为DeepSeek
   PRIMARY_PROVIDER=deepseek
   
   # 添加DeepSeek API密钥
   DEEPSEEK_API_KEY=你的实际API密钥
   ```

### 3. 验证配置

启动应用并检查日志确认DeepSeek提供商已正确加载：

```bash
# Windows
.\start.ps1

# Linux/macOS  
bash start.sh
```

## DeepSeek 模型说明

项目已配置了以下DeepSeek模型：

### deepseek-chat
- **用途**：通用对话和分析任务
- **上下文长度**：32,768 tokens
- **适用场景**：投资分析、市场研究、策略讨论

### deepseek-coder  
- **用途**：代码生成和编程任务
- **上下文长度**：16,384 tokens
- **适用场景**：交易策略编写、技术指标开发

## 重要注意事项

### 嵌入模型限制
DeepSeek目前不提供嵌入（embedding）模型。如果你需要使用需要嵌入功能的高级特性（如知识库检索），建议：

1. **配置备用提供商**：添加SiliconFlow或其他支持嵌入的提供商
2. **混合使用**：DeepSeek用于主要推理，其他提供商用于嵌入

示例配置：
```bash
# 主要提供商（推理任务）
PRIMARY_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的密钥

# 备用提供商（嵌入任务）
SILICONFLOW_API_KEY=你的SiliconFlow密钥
```

### 成本优化
DeepSeek提供极具竞争力的价格：
- 相比OpenAI GPT-4，成本降低约90%
- 性能接近GPT-4水平
- 支持中文优化

### 地区可用性
DeepSeek在以下地区可用：
- 中国大陆
- 亚太地区
- 欧洲
- 其他大部分地区

## 故障排除

### 常见问题

1. **API密钥无效**
   - 确认从正确的URL获取密钥
   - 检查密钥格式是否正确
   - 验证账户余额

2. **连接超时**
   - 检查网络连接
   - 确认防火墙设置
   - 尝试使用代理（如需要）

3. **模型不可用**
   - 确认配置文件中的模型ID正确
   - 检查DeepSeek服务状态
   - 查看详细错误日志

### 日志检查

查看应用日志获取详细错误信息：
```bash
# 检查最新日志
ls logs/
cat logs/最新时间戳/*.log
```

## 高级配置

### 自定义模型参数

在智能体配置文件中，你可以覆盖默认参数：

```yaml
# 例如在 python/configs/agents/super_agent.yaml 中
models:
  primary:
    model_id: "deepseek-chat"
    provider: "deepseek"
    parameters:
      temperature: 0.3  # 更保守的输出
      max_tokens: 8192  # 更长的响应
```

### 环境变量覆盖

使用环境变量动态调整配置：
```bash
# 临时更改模型
export SUPER_AGENT_MODEL_ID="deepseek-coder"

# 调整温度参数
export SUPER_AGENT_TEMPERATURE=0.1
```

## 支持

如果在配置DeepSeek时遇到问题：

1. 检查本文档的故障排除部分
2. 查看项目的GitHub Issues
3. 在Discord社区寻求帮助
4. 提交新的Issue报告问题

---

**注意**：请妥善保管你的API密钥，不要将其提交到版本控制系统中。