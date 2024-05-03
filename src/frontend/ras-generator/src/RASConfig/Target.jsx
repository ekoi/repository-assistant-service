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
  const bridgeModuleClassOptionalValues = [
    "DansSwordDepositor",
    "DataverseIngester",
    "SwhApiDepositor",
    "SwhSwordDepositor",
    "ZenodoApiDepositor",
    "FileSystem",
    "Mail",
    "PoC- B2Share",
    "PoC-iRODS",
    "PoC-PPRINT",
  ]
  const [currFields, setCurrFields] = useState({
    "repo-name": "ssh.datastations.nl",
    "repo-display-name": "SSH Datastation",
    "bridge-module-class": "DansSwordDepositor",
    "base-url": "https://ssh.datastations.nl",
    "target-url": "https://sword2.ssh.datastations.nl/collection/1",
    username: "API_KEY",
    password: "",
    metadata: {
      specification: [],
      "transformed-metadata": [],
    },
  })
  const addMetadata = () => {
    currFields["metadata"]["transformed-metadata"].push({})
    setCurrFields({ ...currFields })
    fields[baseKey][index] = currFields
    setFields({ ...fields })
  }
  const onChangeFieldTransformedMetadata = (e, v, i) => {
    currFields["metadata"]["transformed-metadata"][i][v] = e.target.value
    setCurrFields({ ...currFields })
    fields[baseKey][index] = currFields
    setFields({ ...fields })
  }
  const onDeleteTransformedMetadata = (i) => {
    currFields["metadata"]["transformed-metadata"].splice(i, 1)
    setCurrFields({ ...currFields })
  }
  const onChangeFields = (e, v) => {
    currFields[v] = e.target.value
    setCurrFields({ ...currFields })
    fields[baseKey][index] = currFields
    setFields({ ...fields })
  }
  const onDelete = (index) => {
    fields[baseKey].splice(index, 1)
    setFields({ ...fields })
  }
  const addNotification = () => {
    currFields["notification"].push({})
    setCurrFields({ ...currFields })
  }
  return (
    <Card {...otherProps}>
      <Card.Header>
        Target # {index}
        <ButtonGroup size="sm" style={{ float: "right" }}>
          <Button color="danger" onClick={() => onDelete(index)}>
            Delete
          </Button>
        </ButtonGroup>
      </Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>repo-name</Form.Label>
          <Form.Control
            type="text"
            name="repo-name"
            placeholder="..."
            value={currFields["repo-name"]}
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
            value={currFields["repo-display-name"]}
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "repo-display-name")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group
          className="mb-3"
          controlId="formBasicEmail"
          value={currFields["bridge-module-class"]}
          onChange={(e) => {
            onChangeFields(e, "bridge-module-class")
          }}
        >
          <Form.Label>bridge-module-class</Form.Label>
          <Form.Select aria-label="Default select example">
            <option value={""}>Open this select menu</option>
            {bridgeModuleClassOptionalValues.map((v, i) => {
              return (
                <option value={v} key={i}>
                  {v}
                </option>
              )
            })}
          </Form.Select>

          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>base-url</Form.Label>
          <Form.Control
            type="text"
            name="base-url"
            value={currFields["base-url"]}
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
            value={currFields["target-url"]}
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
            value={currFields["username"]}
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
            value={currFields["password"]}
            placeholder="..."
            onChange={(e) => {
              onChangeFields(e, "password")
            }}
          />
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>
            metadata{" "}
            <Button size="sm" color="default" onClick={() => addMetadata()}>
              Add Metadata
            </Button>
          </Form.Label>
          <br></br>
          {currFields["metadata"]["transformed-metadata"]?.length > 0 && (
            <Table>
              <thead>
                <tr>
                  <td>name</td>
                  <td>transformer-url</td>
                  <td>target-dir</td>
                </tr>
              </thead>
              <tbody>
                {currFields?.metadata["transformed-metadata"].map((v, i) => {
                  return (
                    <tr key={i}>
                      <td>
                        <Form.Control
                          type="text"
                          name="name"
                          value={v.name || ""}
                          placeholder="..."
                          onChange={(e) => {
                            onChangeFieldTransformedMetadata(e, "name", i)
                          }}
                        />
                      </td>
                      <td>
                        <Form.Control
                          type="text"
                          name="transformer-url"
                          value={v["transformer-url"] || ""}
                          placeholder="..."
                          onChange={(e) => {
                            onChangeFieldTransformedMetadata(
                              e,
                              "transformer-url",
                              i
                            )
                          }}
                        />
                      </td>
                      <td>
                        <Form.Control
                          type="text"
                          name="target-dir"
                          value={v["target-dir"] || ""}
                          placeholder="..."
                          onChange={(e) => {
                            onChangeFieldTransformedMetadata(e, "target-dir", i)
                          }}
                        />
                      </td>
                      <td>
                        <Button
                          color="danger"
                          size="sm"
                          onClick={() => {
                            onDeleteTransformedMetadata(i)
                          }}
                        >
                          Delete
                        </Button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </Table>
          )}
          {currFields["metadata"]["transformed-metadata"].length == 0 && (
            <>
              <Badge color="info">No Data</Badge>{" "}
            </>
          )}
          <Form.Text className="text-muted"></Form.Text>
        </Form.Group>
      </Card.Body>
    </Card>
  )
}
export default Target
