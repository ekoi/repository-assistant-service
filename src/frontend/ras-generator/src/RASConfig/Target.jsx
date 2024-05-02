import { useState } from "react"
import {
  Badge,
  Button,
  ButtonGroup,
  Card,
  CardBody,
  Form,
  Table,
} from "react-bootstrap"

const Target = (props) => {
  const { fields, setFields, index, ...otherProps } = props
  const baseKey = "targets"
  const [currFields, setCurrFields] = useState({
    "repo-name": "",
    "service-url": "",
    "result-url": "",
    notification: [],
  })
  const onChangeFields = (e, v) => {
    currFields[v] = e.target.value
    setCurrFields({ ...currFields })
    fields[baseKey][index] = currFields
    setFields({ ...fields })
  }
  const onDelete = (index)=>{
    fields[baseKey].splice(index,1);
    setFields({...fields})
  }
  const addNotification = () => {
    currFields["notification"].push({})
    setCurrFields({ ...currFields })
  }
  return (
    <Card {...otherProps}>
      <Card.Header>
        Target # {index}
        <ButtonGroup size="sm" style={{float:"right"}}>
          <Button color="danger" onClick={()=>onDelete(index)}>Delete</Button>
        </ButtonGroup>
      </Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>repo-name</Form.Label>
          <Form.Control
            type="text"
            name="repo-name"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "repo-name")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>repo-display-name</Form.Label>
          <Form.Control
            type="text"
            name="repo-display-name"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "repo-display-name")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>bridge-module-class</Form.Label>
          <Form.Control
            type="text"
            name="bridge-module-class"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "bridge-module-class")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>base-url</Form.Label>
          <Form.Control
            type="text"
            name="base-url"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "base-url")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>target-url</Form.Label>
          <Form.Control
            type="text"
            name="target-url"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "target-url")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>username</Form.Label>
          <Form.Control
            type="text"
            name="username"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "username")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>password</Form.Label>
          <Form.Control
            type="text"
            name="password"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "password")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>    

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>notications</Form.Label>
          <br></br>
          {currFields?.notification?.length > 0 && (
            <Table>
              <thead>
                <tr>
                  <td>type</td>
                  <td>conf</td>
                </tr>
              </thead>
              <tbody>
                {currFields?.notification?.map((v, i) => {
                  ;<tr>
                    <td>{v.type}</td>
                    <td>{v.conf}</td>
                  </tr>
                })}
              </tbody>
            </Table>
          )}
          {currFields?.notification?.length == 0 && (
            <>
              <Badge color="info">No Data</Badge>{" "}
              <Button size="sm" color="default" onClick={() => addNotification}>
                Add Notification
              </Button>
            </>
          )}
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
      </Card.Body>
    </Card>
  )
}
export default Target
