import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; 
import Question from './Question/Question';
import { fetchData } from '../common/api'; 
import './Quiz.css';

function Quiz() {
  const { id } = useParams(); 
  const { title } = useParams();
  const decodedTitle = decodeURIComponent(title);
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [data, setData] = useState([]);
  const [hintIndex, setHintIndex] = useState(0);
  const [isLoading, setLoading] = useState(true);  // 画像のローディング状態を追跡
  const [error, setError] = useState(null);


  useEffect(() => {
    const loadData = async () => {
      
      // const paddedData = result.map(item => {
      //   let paddedExplanation = item.explanation;
      //   if (paddedExplanation.length < 1000) {
      //     paddedExplanation += ' '.repeat(1000 - paddedExplanation.length);
      //   } else if (paddedExplanation.length > 1000) {
      //     paddedExplanation = paddedExplanation.substring(0, 1000);
      //   }
      //   return { ...item, explanation: paddedExplanation };
      // });
      // setData(paddedData);
      
      try {
        setLoading(true);
        const result = await fetchData(`quiz/${id}`); 
        setData(result);
      } catch (err) {
        setError('データの取得に失敗しました。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [id]); 

  useEffect(() => {
    setShowAnswer(false);
  }, [currentQuestionIndex]);

  const handleNextQuestion = () => {
    if (currentQuestionIndex < data.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setHintIndex(0); // ヒントインデックスを 0 にリセット 
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      setHintIndex(0); // ヒントインデックスを 0 にリセット 
    }
  };

  const handleAnswerToggle = () => {
    setShowAnswer(prevState => !prevState);
  };

  const handleBack = () => {
    navigate('/quizset');
  };


  // ヒントを次へ進めるハンドラ
  const showNextHint = () => {
      if (hintIndex < data[currentQuestionIndex].hints.length) {
      setHintIndex(hintIndex + 1); // ヒントインデックスを増やす
      }};



  return (
    <div className="Quiz">
      <div className="quiz-header">
        <h1>{decodedTitle}関連 </h1>
        <div className="progress-indicator">
                        問題 {currentQuestionIndex + 1} / {data.length}
        </div>
        <button className="back-button" onClick={handleBack} style={{ margin: '10px' }}>戻る</button>
      </div>
      <main>
        <div className="quiz-container">
          {data.length > 0 && (
            <Question
              data={data[currentQuestionIndex]}
              showAnswer={showAnswer}
              onAnswer={handleAnswerToggle}
              onNext={handleNextQuestion}
              onPrevious={handlePreviousQuestion}
              currentQuestionIndex={currentQuestionIndex}
              totalQuestions={data.length}
              hintIndex={hintIndex}
              showNextHint={showNextHint}
              isLoading={isLoading}
              setLoading={setLoading}
            />
          )}
        </div>
      </main>
    </div>
  );
}

export default Quiz;