import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';
import { useAuth } from './AuthContext';
let axiosInterceptorId;

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const { login } = useAuth(); 

// ログイン成功時に実行
const setAxiosInterceptor = (token) => {
    return new Promise((resolve, reject) => {
        if (axiosInterceptorId) {
            axios.interceptors.request.eject(axiosInterceptorId);
        }

        axiosInterceptorId = axios.interceptors.request.use(
            config => {
                config.headers['Authorization'] = `Bearer ${token}`;
                return config;
            },
            error => {
                reject(error);
                return Promise.reject(error);
            }
        );
        resolve();
    });
};
const handleLogin = async (event) => {
    event.preventDefault();
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await axios.post(`${process.env.REACT_APP_API_URL}/auth/login`, formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        // トークンを保存してからインターセプターを設定し、完了を待つ
        const token = response.data.access_token;
        console.log('Login successful:');
        await setAxiosInterceptor(token);  // 完了を待つ
        login(token);
        navigate('/quizset');
    } catch (error) {
        console.error('Login failed:', error);
    }
};

return (
    <div className="form-container">
        <form onSubmit={handleLogin}>
            <div className="form-input">
                <label>Username:</label>
                <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
            </div>
            <div className="form-input">
                <label>Password:</label>
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <button type="submit" className="form-button">Login</button>
        </form>
    </div>
);
}
