export default function Home() {
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
        <form className="flex flex-col gap-4">
          <input
            className="border border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            type="file"
            name="file"
          />
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
