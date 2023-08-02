import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import News from './News';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<News />}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
