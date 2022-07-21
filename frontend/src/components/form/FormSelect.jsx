import Form from "react-bootstrap/Form";

export default function FormSelect(props) {
  return (
    <Form.Group className="mb-3" controlId={`form-${props.name}`}>
      <Form.Label>{props.label}</Form.Label>
      <Form.Select name={props.name} onChange={props.onChange} value={props.value}>
        {props.children}
      </Form.Select>
    </Form.Group>
  );
}
