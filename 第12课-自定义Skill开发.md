# 第12课：自定义Skill开发

## 课程目标
- 理解Skill结构
- 掌握Skill开发流程
- 学会集成第三方API
- 发布Skill到社区

---

## 第一部分：Skill结构（20分钟）

### 1.1 Skill目录结构

```
my-skill/
├── SKILL.md          # Skill说明（Agent会读取）
├── package.json      # 依赖声明
├── scripts/          # 可执行脚本
│   ├── main.sh
│   └── helper.py
└── assets/           # 资源文件
    └── template.txt
```

### 1.2 SKILL.md规范

```markdown
# My Skill

## 功能
这个Skill可以做什么

## 使用方法
如何使用这个Skill

## 示例
具体的使用示例

## 依赖
需要安装的依赖
```

---

## 第二部分：开发流程（40分钟）

### 2.1 创建Skill

```bash
# 创建目录
mkdir ~/.openclaw/skills/my-skill
cd ~/.openclaw/skills/my-skill

# 创建文件
touch SKILL.md package.json
mkdir scripts assets
```

### 2.2 编写脚本

```bash
# scripts/main.sh
#!/bin/bash
echo "Hello from my skill!"
```

### 2.3 测试Skill

```bash
# 重启Gateway加载Skill
openclaw gateway restart

# 测试
openclaw chat "使用my-skill"
```

---

## 第三部分：集成第三方API（40分钟）

### 3.1 API集成示例

```python
# scripts/api_call.py
import requests
import sys

def call_api(query):
    response = requests.get(
        "https://api.example.com/search",
        params={"q": query}
    )
    return response.json()

if __name__ == "__main__":
    query = sys.argv[1]
    result = call_api(query)
    print(result)
```

### 3.2 配置API密钥

```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "apiKey": "${MY_SKILL_API_KEY}"
      }
    }
  }
}
```

---

## 第四部分：发布Skill（30分钟）

### 4.1 打包Skill

```bash
# 创建README
echo "# My Skill" > README.md

# 初始化git
git init
git add .
git commit -m "Initial commit"
```

### 4.2 发布到GitHub

```bash
# 创建仓库
gh repo create my-skill --public

# 推送代码
git push origin main
```

### 4.3 提交到ClaHub

访问 https://clawhub.com 提交你的Skill

---

## 作业与练习

### 作业1：开发简单Skill（必做）
开发一个Hello World Skill

### 作业2：API集成（必做）
集成一个第三方API

### 作业3：发布Skill（选做）
发布Skill到GitHub和ClaHub

---

## 课程总结

### 本节课你学到了：
✅ Skill结构和规范  
✅ Skill开发流程  
✅ API集成方法  
✅ Skill发布流程  

### 关键要点：
1. **SKILL.md是核心**
2. **脚本要可执行**
3. **API密钥要安全**
4. **测试要充分**

---

**下节课见！** 🚀
