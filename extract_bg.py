with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'url("data:image/png;base64,'
start = content.find(marker) + len(marker)
end = content.find('")', start)
b64_data = content[start:end]
print('Found b64 data, length:', len(b64_data))

with open('app/hero_web.b64', 'w') as f:
    f.write(b64_data)
print('Saved hero_web.b64')
