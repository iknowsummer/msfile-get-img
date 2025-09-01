# Next.js Frontend Dockerfile
FROM node:22-alpine

# 作業ディレクトリ作成
WORKDIR /app

# 依存関係インストール
COPY ./package.json ./package-lock.json* ./
RUN npm install --omit=dev 

# 必要なファイル・ディレクトリのみコピー
COPY .env.local ./
COPY app ./app
COPY public ./public
COPY next.config.ts ./

RUN npm run build

# 3000番で起動
EXPOSE 3000
CMD ["npm", "run", "start"]
