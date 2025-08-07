export default function Home() {
  return (
    <main>
      <h1>Officeファイルから画像取り出し</h1>
      <p>docx, pptx, xlsxファイルを送信してください。</p>
      <p>含まれる画像を抽出します。（zipファイルでダウンロード）</p>
      <form>
        <input
          className="border border-gray-300 rounded p-2"
          type="file"
          name="file"
        />
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded"
          type="submit"
        >
          送信
        </button>
      </form>
    </main>
  );
}
