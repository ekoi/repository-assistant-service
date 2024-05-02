import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button,Badge,Container,Row,Col,Stack } from 'react-bootstrap';
import RasGenerator from './RASConfig/RASGenerator';
function App() {

  return (
    <div className="App">
      <RasGenerator/>
    </div>
  );
}

export default App;
