import axios from "axios";
import { API_URL } from "constants";
import { sleeper } from "utils";
import { Container, Form, Table } from "react-bootstrap";

export default function Signin() {

    function Signinpost(data) {
        const fetch = axios
        .post(`${API_URL}/events/`,data)
        .then(sleeper(500))
        .then((response) => {
          console.log(response.data);
          const res =
            response.data?.map((eve) => ({
              value: eve.id,
              label: eve.name,
              data: eve,
            })) ?? []; 
        })
        .finally(() => {
          //setIsLoading(false);
        });
    }

  return (
    <form id="signinform">
      <div>
      <label>Enter your Username:
        <input type="text" />
      </label>
      </div>
      <div>
      <label>Password:
        <input type="password" />
      </label>
      </div>
      <button  id="submit-btn" type="button" onClick={Signinpost}> Register</button>
    </form>
    // <Container style={{ padding: "16px", position: "relative" }}>
    
    //     <Form name="hinchaForm" method="post">
    //     <InputWrapper>
    //     name="username"
        
    //     </InputWrapper>
    //     {/* <input type="text" name="Username" id="Username" maxlength="80" required> </input>
    //     <input type="hidden" name="Password" id="Password" maxlength="80" required> </input> */}

    //     </Form>

    // </Container>
  );
}