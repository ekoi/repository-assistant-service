import { ChangeEvent, useState } from "react"
import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Col,
  Container,
  Form,
  FormGroup,
  Row,
  Stack,
  Table,
} from "react-bootstrap"
import { Fragment } from "react/jsx-runtime"
import Target from "./Target"
import Enrichment from "./Enrichment"
import FileConversion from "./FileConversion"

const RasGenerator = () => {
  const [fields, setFields] = useState({
    "assistant-config-name": "",
    "description": "",
    "app-name": "",
    "app-config-url": "",
    "targets": [{}],
    "file-conversions": [],
    "enrichments": [],
  })
  const onAddTarget = () => {
    fields["targets"].push({})
    setFields({ ...fields })
  }
  
  const onAddEnrichment = () => {
    fields["enrichments"].push({
      
    })
    setFields({ ...fields })
  }
  const onAddFileConversion = () => {
    fields["file-conversions"].push({})
    setFields({ ...fields })
  }
  
  const downloadFile = () => {
    const fileName = "ras-config"
    const json = JSON.stringify(fields, null, 2)
    const blob = new Blob([json], { type: "application/json" })
    const href = URL.createObjectURL(blob)

    // create "a" HTLM element with href to file
    const link = document.createElement("a")
    link.href = href
    link.download = fileName + ".json"
    document.body.appendChild(link)
    link.click()

    // clean up "a" element & remove ObjectURL
    document.body.removeChild(link)
    URL.revokeObjectURL(href)
  }
  const onChangeFields = (e, key) => {
    fields[key] = e.target.value
    setFields({ ...fields })
  }
  return (
    <Container fluid style={{ textAlign: "left" }}>

      <Row>
        <Col>
          <Card>
            <CardHeader>RAS - Generator</CardHeader>
            <CardBody>
              <Form>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>assistant-config-name</Form.Label>
                  <Form.Control
                    type="text"
                    name="assistant-config-name"
                    value={fields["assistant-config-name"]||" "}
                    placeholder="..."
                    onChange={(e) => {
                      onChangeFields(e, "assistant-config-name")
                    }}
                  />
                  <Form.Text className="text-muted"></Form.Text>
                </Form.Group>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>description</Form.Label>
                  <Form.Control
                    type="text"
                    name="description"
                    value={fields["description"]||" "}
                    placeholder="..."
                    onChange={(e) => {
                      onChangeFields(e, "description")
                    }}
                  />
                  <Form.Text className="text-muted"></Form.Text>
                </Form.Group>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>app-name</Form.Label>
                  <Form.Control
                    type="text"
                    name="app-name"
                    value={fields["app-name"]||" "}
                    placeholder="..."
                    onChange={(e) => {
                      onChangeFields(e, "app-name")
                    }}
                  />
                  <Form.Text className="text-muted"></Form.Text>
                </Form.Group>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label>app-config-url</Form.Label>
                  <Form.Control
                    type="text"
                    name="app-config-url"
                    value={fields["app-config-url"]||" "}
                    placeholder="..."
                    onChange={(e) => {
                      onChangeFields(e, "app-config-url")
                    }}
                  />
                  <Form.Text className="text-muted"></Form.Text>
                </Form.Group>
              </Form>
              <hr></hr>
              <hr></hr>
              <Button color="primary" size="sm" onClick={onAddTarget}>
                Add Target, Total: {fields["targets"].length}
              </Button><br></br><br></br>
              {fields["targets"].map((v, i) => {
                return (
                  <Target  style={{marginTop:"10px"}}
                    key={i}
                    index={i}
                    fields={fields}
                    setFields={setFields}
                  ></Target>
                )
              })}
              {!fields["targets"] && (
                <tr>
                  <td>
                    <>No Data</>
                  </td>
                </tr>
              )}
              <hr></hr>
              <Button color="primary" size="sm" onClick={onAddFileConversion}>
                Add File Conversion, Total: {fields["file-conversions"].length}
              </Button><br></br><br></br>
              {fields["file-conversions"].map((v, i) => {
                return (
                  <FileConversion  style={{marginTop:"10px"}}
                    key={i}
                    index={i}
                    fields={fields}
                    setFields={setFields}
                  ></FileConversion>
                )
              })}
              {!fields["file-conversions"] && (
                <tr>
                  <td>
                    <>No Data</>
                  </td>
                </tr>
              )}
              <hr></hr>
              <Button color="primary" size="sm" onClick={onAddEnrichment}>
                Add Enrichments, Total: { fields["enrichments"].length}
              </Button>
              {fields["enrichments"].map((v, i) => {
                return (
                  <Enrichment style={{marginTop:"10px"}}
                    key={i}
                    index={i}
                    fields={fields}
                    setFields={setFields}
                  ></Enrichment>
                )
              })}
              {!fields?.enrichments && (
                <tr>
                  <td>
                    <>No Data</>
                  </td>
                </tr>
              )}
            </CardBody>
            <CardFooter>
              <Button
                style={{ float: "right" }}
                variant="primary"
                onClick={downloadFile}
              >
                Generate JSON
              </Button>
            </CardFooter>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}
export default RasGenerator
