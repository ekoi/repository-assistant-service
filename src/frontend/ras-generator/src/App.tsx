import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button,Badge,Container,Row,Col,Stack } from 'react-bootstrap';
function App() {
  return (
    <div className="App">
      <Container fluid>
      <Row>
        <Col><h1>
        RAS - Generator
      </h1>
      <br></br>
      <Stack direction="horizontal" gap={2}>
              <Button as="a" variant="primary">
                Generate JSON
              </Button>
      </Stack>;</Col>
      </Row>
    </Container>
      
    </div>
  );
}

export default App;
