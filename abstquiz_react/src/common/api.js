import axios from 'axios';

export const fetchData = async (path) => {
    // 環境変数からAPIのベースURLを読み込む
    const baseUrl = process.env.REACT_APP_API_URL;
    console.log(`${baseUrl}/${path}`);
  try {
    const response = await axios.get(`${baseUrl}/${path}`);
    return response.data;
  } catch (error) {
    // 401エラーの場合はログインページにリダイレクとする
    if (error.response.status === 401) {
      window.location.href = '/login';
    }
    // エラー発生時はコンソールにエラーを出力し、空の配列を返す
    return [];
  }
}