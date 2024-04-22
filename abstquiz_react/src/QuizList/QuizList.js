import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { fetchData } from '../common/api';
import './QuizList.css';

function QuizList() {
  const [quizsets, setQuizsets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getQuizSets = async () => {
      try {
        setLoading(true);
        const quizData = await fetchData('quizsets');
        setQuizsets(quizData);
      } catch (err) {
        setError('データの取得に失敗しました。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    getQuizSets();
  }, []);

  const renderedQuizSets = useMemo(() => (
    quizsets.map(quizset => (
      <li key={quizset.id}>
        <Link to={`/quizset/${quizset.id}/${encodeURIComponent(quizset.title)}`}>
          {quizset.title}
        </Link>
      </li>
    ))
  ), [quizsets]);

  if (loading) return <div className="loader"></div>;
  if (error) return <p>エラー: {error}</p>;

  return (
    <div className="container">
      <h1>抽象イメージクイズ</h1>
      <p className="app-description">
      画像が何の概念を表しているのをか当てるクイズです。<br/>
      概念を視覚化した画像を通じて、概念の多様な側面に気付き、より深い理解と持続的な記憶を促進します(?)。
      </p>
      <h2>問題集一覧</h2>
      <ul>
        {renderedQuizSets}
      </ul>
    </div>
  );
}

export default QuizList;
