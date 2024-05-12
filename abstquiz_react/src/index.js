import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import QuizList from './QuizList/QuizList';  // クイズ一覧コンポーネント
import Quiz from './Quiz/Quiz';  // クイズ実施コンポーネント
import './App.css'; 
import LoginPage from './auth/LoginPage';
import { AuthProvider } from './auth/AuthContext';
import { useAuth } from './auth/AuthContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
function ProtectedRoute({ children }) {
  const { authToken } = useAuth();
  return authToken ? children : <Navigate to="/login" />;
}

root.render(
  <React.StrictMode>
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<App />}>
            <Route index element={<QuizList />} />
            <Route path="quizset" element={
              <ProtectedRoute>
                <QuizList />
              </ProtectedRoute>} />
            <Route path="quizset/:id/:title" element={
              <ProtectedRoute>
                <Quiz />
              </ProtectedRoute>
            } />
            <Route path="login" element={<LoginPage />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
