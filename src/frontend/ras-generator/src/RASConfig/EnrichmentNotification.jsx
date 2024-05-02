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

const EnrichmentNotification = (props) => {
  const { fields, setFields, index, ...otherProps } = props
  const baseKey = "enrichments"
  const [currFields, setCurrFields] = useState({
    "type": "",
    "conf": "",
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
  const onSave = () => {
    fields[baseKey][index] = currFields
    setFields({ ...fields })
  }
  return (
    <Card {...otherProps}>
      <Card.Header>
        Enrichment # {index}
        <ButtonGroup size="sm" style={{float:"right"}}>
          <Button color="danger" onClick={()=>onDelete(index)}>Delete</Button>
        </ButtonGroup>
      </Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>name</Form.Label>
          <Form.Control
            type="text"
            name="name"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "name")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>service-url</Form.Label>
          <Form.Control
            type="text"
            name="service-url"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "service-url")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
      </Card.Body>
    </Card>
  )
}
export default EnrichmentNotification
