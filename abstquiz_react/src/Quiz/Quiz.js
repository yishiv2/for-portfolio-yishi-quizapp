import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; 
import Question from './Question/Question';
import { fetchData } from '../common/api'; 
import './Quiz.css';

import Hint from './Hint/Hint';

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


  useEffect(() => {
    const loadData = async () => {
      
      try {
        setLoading(true);
        const result = await fetchData(`quiz/${id}`); 
        setData(result);
      } catch (err) {
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


      // レンダリング部分
      if (!data) {
        return <div>Loading...</div>; // データがまだ利用できない場合はローディングメッセージを表示
      }
    

  // ヒントを次へ進めるハンドラ
  const showNextHint = () => {
    if (hintIndex < data[currentQuestionIndex].hints.length) {
    setHintIndex(hintIndex + 1); // ヒントインデックスを増やす
    }};


  if (data.length === 0) {
      return <div className="loader"></div>;
  }

  return (
    <div className="Quiz">
      <div className="quiz-header">
        <h1>{decodedTitle}関連 </h1>
        
          <div className="progress-indicator">
                          問題 {currentQuestionIndex + 1} / {data.length}
          </div>
          <button className="back-button" onClick={handleBack} style={{ margin: '10px' }}>戻る</button>
          {data.length > 0 && (
            <Hint hintIndex={hintIndex} showNextHint={showNextHint} hints={data[currentQuestionIndex].hints} />
          )}
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