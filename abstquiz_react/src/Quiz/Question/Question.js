import React from 'react';
import './Question.css';



function Question({ data, showAnswer, onAnswer, onNext, onPrevious, currentQuestionIndex, totalQuestions, isLoading, setLoading}) {
    // 画像をクリックしたときに答えの表示状態を切り替えるハンドラ
    const toggleAnswer = () => {
        onAnswer(!showAnswer); // 現在の showAnswer の反対の値をセット
    };

    return (
        <div className='outline'>
            <div className="image-hint-container">
                <div className="image-container">
                    {currentQuestionIndex > 0 && (
                        <div className="nav-button left" onClick={onPrevious}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="15 18 9 12 15 6"></polyline>
                            </svg>
                        </div>
                    )}
                    <div className="inner-image-container">
                        {isLoading ? (
                            <div className="loader"></div>  // ローディングインジケーターを表示
                        ) : (
                            <img src={`${data.image}`} alt="Quiz" style={{ width: "1024px", height: "1024px" }} onClick={toggleAnswer} onLoad={() => setLoading(false)} />
                        )}
                        <div
                            style={{
                                opacity: !showAnswer ? 1 : 0,
                                visibility: !showAnswer ? 'visible' : 'hidden',
                                color: 'black',
                                backgroundColor: 'white',
                                marginLeft: '1px',
                            }}
                        >
                            画像をクリックすると解答が表示されます
                        </div>
                    </div>
                    {currentQuestionIndex < totalQuestions - 1 && (
                        <div className="nav-button right" onClick={onNext}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="9 18 15 12 9 6"></polyline>
                            </svg>
                        </div>
                    )}
                </div>

            </div>
           { showAnswer && (
            <div className="answer-container">
                <p className="answer-text"><span>{data.answer}</span></p>
                <p className="answer-explanation" style={{ whiteSpace: 'pre-wrap' }}>{data.explanation}</p>
            </div>
            )}
        </div>
    );
}

export default Question;
