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

const FileConversion = (props) => {
  const { fields, setFields, index, ...otherProps } = props
  const baseKey = "file-conversions"
  const [currFields, setCurrFields] = useState({
    "origin-type": "",
    "target-type": "",
    "conversion-url": "",
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
    <Card  {...otherProps}>
      <Card.Header>
        File Conversion # {index}
        <ButtonGroup size="sm" style={{float:"right"}}>
          <Button color="danger" onClick={()=>onDelete(index)}>Delete</Button>
        </ButtonGroup>
      </Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>origin-type</Form.Label>
          <Form.Control
            type="text"
            name="origin-type"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "origin-type")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>target-type</Form.Label>
          <Form.Control
            type="text"
            name="target-type"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "target-type")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>conversion-url</Form.Label>
          <Form.Control
            type="text"
            name="conversion-url"
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "conversion-url")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
      </Card.Body>
    </Card>
  )
}
export default FileConversion
