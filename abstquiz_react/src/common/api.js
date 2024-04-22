import axios from 'axios';

export const fetchData = async (path) => {
    // 環境変数からAPIのベースURLを読み込む
    const baseUrl = process.env.REACT_APP_API_URL;
  try {
    const response = await axios.get(`${baseUrl}/${path}`);
    return response.data;
  } catch (error) {
    // エラー発生時はコンソールにエラーを出力し、空の配列を返す
    console.error('Error fetching data:', error);
    return [];
  }
}