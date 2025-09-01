"use client";

import React, { useState } from "react";

export default function Home() {
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    try {
      const input = (e.target as HTMLFormElement).elements.namedItem(
        "file"
      ) as HTMLInputElement;
      if (!input.files?.[0]) return;

      const formData = new FormData();
      formData.append("file", input.files[0]);

      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
      const res = await fetch(`${apiBaseUrl}/extract-office-media`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`サーバーエラー: ${res.status}`);
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "mediafiles.zip";
      a.click();

      URL.revokeObjectURL(url);
    } catch (_err: unknown) {
      setError("通信エラー。サーバーから応答がありません。");
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center text-blue-700">
          Officeファイルから画像取り出し
        </h1>
        <p className="mb-1 text-center text-gray-700">
          docx, pptx, xlsxファイルを送信してください。
        </p>
        <p className="mb-6 text-center text-gray-500 text-sm">
          含まれる画像を抽出します。（zipファイルでダウンロード）
        </p>
        <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
          <input
            className="border border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            type="file"
            name="file"
          />
          {error && (
            <div className="mb-4 text-red-600 text-center border border-red-300 bg-red-50 rounded p-2">
              {error}
            </div>
          )}
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition-colors duration-200"
            type="submit"
          >
            送信
          </button>
        </form>
      </div>
    </main>
  );
}
