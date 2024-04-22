import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import QuizList from './QuizList/QuizList';  // クイズ一覧コンポーネント
import Quiz from './Quiz/Quiz';  // クイズ実施コンポーネント
import './App.css'; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<QuizList />} />
          <Route path="quizset" element={<QuizList />} />
          <Route path="quizset/:id/:title" element={<Quiz />} />
        </Route>
      </Routes>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
