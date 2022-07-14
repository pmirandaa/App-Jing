import React from 'react';
import ReactDOM from 'react-dom';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import 'index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import App from 'App';
import reportWebVitals from 'reportWebVitals';
import News from 'pages/News';
import Messages from 'pages/Messages';
import Info from 'pages/Info';
import Matches from 'pages/Matches';
import Teams from 'pages/Teams';
import Admin from 'pages/Admin';

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} >
          <Route index element={<News />} />
          <Route path="personas" element={<Info/>} />
          <Route path="partidos" element={<Matches/>} />
          <Route path="equipos" element={<Teams/>} />
          <Route path="mensajes" element={<Messages/>} />
          <Route path="administracion" element={<Admin/>} />
        </Route>
        
        <Route path="/hola" element={<Teams />} />
        <Route path="*" element={<Navigate to="/" replace={true} />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
