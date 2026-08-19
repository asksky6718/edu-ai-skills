---
name: zhixunbao-admin-core
description: 网校管理后台公共基础技能。提供后台登录、会话保持、CSRF 获取、环境安全边界、通用 HTTP/Playwright 调用方式，以及内置 API 通道的使用说明。当需要接管网校后台、调用后台接口、执行后台命令或编写后台自动化操作时触发。
---

# 网校后台公共基础

## 目标

让智能体能够安全、稳定地接管网校管理后台，完成登录、查询、表单提交、状态流转和结果验证。本技能只涉及后台管理操作，不涉及代码开发。

## 环境

| 环境 | 后台地址 | 说明 |
|---|---|---|
| 开发 | `${ZXB_BASE_URL}/admin` | 默认操作环境 |
| 生产 | 生产域名/admin | 只读巡检；写操作需明确授权 |

默认只操作开发环境；生产环境必须得到用户明确授权后才可执行写操作。

## 安全红线

1. 禁止直接写数据库；所有写操作必须走后台 Service、HTTP 表单或已有 Console 命令。
2. 禁止修改系统保护账号的密码、邮箱、角色等。
3. 发布、关闭、删除、发证、批量导入等高危操作必须：先查询确认对象 → 预检/预览 → 执行 → 验证结果。
4. 操作前确认环境：开发/生产；生产写操作必须用户确认。
5. 凭据优先使用环境变量或安全配置，不写入 Skill 文件、脚本、日志。

## 登录与会话

### 登录表单字段

| 字段 | 说明 |
|---|---|
| 请求地址 | POST `${ZXB_BASE_URL}/login_check` |
| `_username` | 管理员账号 |
| `_password` | 管理员密码 |
| `_csrf_token` | 从登录页 `input[name="_csrf_token"]` 获取 |
| `_remember_me` | 建议 `on` |
| `_target_path` | 建议后台首页路径 |

### curl 示例

```bash
BASE_URL="${ZXB_BASE_URL:-https://your-domain}"
COOKIE="$(mktemp)"
# 1. 获取登录 CSRF
CSRF=$(curl -s -c "$COOKIE" "$BASE_URL/login" | grep -o 'name="_csrf_token" value="[^"]*"' | sed 's/.*value="//;s/"//' | head -1)
# 2. 登录
curl -s -b "$COOKIE" -c "$COOKIE" -X POST "$BASE_URL/login_check" \
  --data-urlencode "_username=${ZXB_ADMIN_USER}" \
  --data-urlencode "_password=${ZXB_ADMIN_PASS}" \
  --data-urlencode "_csrf_token=${CSRF}" \
  --data-urlencode "_remember_me=on" \
  --data-urlencode "_target_path=/admin" \
  -o /dev/null -w '%{http_code}\n'
# 3. 验证登录
curl -s -b "$COOKIE" -L "$BASE_URL/admin" | grep -q 'logout\|退出' && echo "login ok"
```

### 后台表单提交通用方法

- 多数后台表单使用 `input[name="_csrf_token"]`，提交前先 GET 目标页面，从 HTML 中提取同一个 `_csrf_token`。
- 如果接口返回 JSON，优先解析 JSON 中的 `error`/`success`。
- 如果页面有重定向，使用 `-L` 跟随并检查目标页是否出现成功/失败提示。

### 浏览器兜底

复杂 UI（上传、装修、拖拽、富文本）可用 Playwright CLI：

```bash
playwright screenshot --browser chromium --viewport-size=1440,900 "$BASE_URL/admin" /tmp/admin.png
```

## Console 通用命令

```bash
cd "${PROJECT_ROOT:-.}"
${PHP_BIN:-php} app/console --env=dev <command>
```

执行前先 `--help` 确认参数；有 `--execute`/`--real` 之类开关时，先预览后执行。

## 内置 API 通道

### 能力

后台「系统 → API 设置」提供外部应用 API：

- 是否开启外部应用 API 登录。
- AppKey / SecretKey：外部应用凭据。
- IP 白名单：限制来源 IP。

开启后，请求头携带：

```text
Access-Token: md5(AppKey + '-' + SecretKey)
```

### 适合场景

- 已有 API 资源的标准模块查询/部分写操作：课程、用户、订单、班级、资讯、证书、优惠券等。
- 少量插件 API。

### 不适合场景

- 未提供 API 的后台 CRUD，仍需后台表单/浏览器。
- Excel/CSV 文件上传类操作仍需后台页面或专用接口。

### 使用约定

1. 开启 API 前确认 IP 白名单只包含可信执行机 IP。
2. AppKey/SecretKey 必须安全保存，禁止写入仓库。
3. 优先用后台表单完成“业务写操作”，用 API 做“查询/校验/简单写入”。

## 结果验证模板

每次操作完成后输出：

- 操作对象：ID/名称
- 操作类型：查询/创建/更新/发布/删除/导入
- 执行结果：成功/失败/跳过数量
- 验证方式：页面/接口/数据库只读查询
- 环境：dev/prod