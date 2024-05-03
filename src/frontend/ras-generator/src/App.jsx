import React from "react"
import "./App.css"
import "bootstrap/dist/css/bootstrap.min.css"
import { Button, Badge, Container, Row, Col, Stack } from "react-bootstrap"
import RasGenerator from "./RASConfig/RASGenerator"
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom"
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
          <Route
            path="/admin"
            render={(props) => <RasGenerator {...props} />}
          />
        </Switch>
      </BrowserRouter>
    </div>
  )
}

export default App
