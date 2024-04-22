import React from 'react';
import { Outlet ,Link} from 'react-router-dom';
import './App.css'; 


function App() {
  return (
      <>
        <header className="site-header">
          <div className="header-container">
            <h1>(β版)</h1>
            <nav>
              <ul>
                <li style={{ cursor: 'not-allowed' }}>
                  <span style={{ cursor: 'not-allowed', color: '#aaa' }}>Login</span>
                </li>
                <li>
                  <Link to={`/quizset`}>問題集一覧</Link>
                </li>
                <li style={{ cursor: 'not-allowed' }}>
                  <span style={{ cursor: 'not-allowed', color: '#aaa' }}>About Us</span>
                </li>
                <li style={{ cursor: 'not-allowed' }}>
                  <span style={{ cursor: 'not-allowed', color: '#aaa' }}>Contact</span>
                </li>
              </ul>
            </nav>
          </div>
        </header>
        <main>
        <Outlet />  {/* ネストされたルートのコンポーネントが表示される */}
      </main>
      </>

  );
}

export default App;

