import { EventContext } from "contexts/EventContext";
import { useContext, useState } from "react";
import { SwitchTransition, CSSTransition } from "react-transition-group";
import {
  Button,
  ButtonGroup,
  Col,
  Container,
  Image,
  Row,
} from "react-bootstrap";

export default function Maps() {
  const { event } = useContext(EventContext);
  const [activeMap, setActiveMap] = useState(1);

  const data = [
    {
      id: 1,
      name: "Mapa 1",
      image: "/img/mapa1.jpg",
      description: (
        <>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus
            ut turpis libero. Nam faucibus magna at cursus rutrum. Sed nec metus
            lorem. Nullam fringilla sodales libero, eu varius diam congue sed.
            Sed scelerisque dictum nisl ac aliquam. Quisque auctor ligula in
            nisl vestibulum, non pretium dui porta. Donec euismod justo
            imperdiet, malesuada quam sed, consectetur orci. Aliquam erat
            volutpat. Fusce a pharetra arcu, sit amet fringilla dolor. Maecenas
            nisi augue, rutrum id tincidunt in, ornare eu mauris.
          </p>
          <ul>
            <li>Aliquam vel arcu vitae lectus bibendum maximus.</li>
            <li>Aliquam vitae urna nec magna pharetra pretium.</li>
            <li>Etiam ac turpis vitae turpis fermentum cursus.</li>
          </ul>
        </>
      ),
    },
    {
      id: 2,
      name: "Mapa 2",
      image: "/img/mapa2.jpg",
      description: null,
    },
    {
      id: 3,
      name: "Mapa 3",
      image: "/img/mapa3.jpg",
      description: (
        <>
          <p>
            Maecenas pulvinar rutrum leo a fringilla. Aliquam erat volutpat.
            Mauris sapien nibh, pretium eget consequat at, rutrum venenatis
            nunc. Maecenas luctus, lorem eu porttitor consectetur, orci ante
            euismod metus, in ornare felis odio ac elit. Aliquam erat volutpat.
            Vivamus tempor velit sit amet libero dignissim faucibus. Nunc eu
            lorem vitae nunc tristique ultrices a at arcu. Donec scelerisque
            posuere lectus, non tincidunt urna tincidunt hendrerit. Proin
            placerat nibh quis libero tempus, vehicula lacinia ligula eleifend.
            Nam placerat velit tincidunt, egestas diam ornare, posuere nulla.
            Curabitur luctus at dolor in malesuada. Orci varius natoque
            penatibus et magnis dis parturient montes, nascetur ridiculus mus.
            Donec posuere imperdiet leo, in ullamcorper leo consectetur quis.
            Duis volutpat ante sit amet felis tempus molestie. Nunc gravida
            risus arcu, sit amet maximus nibh tempus convallis. Vestibulum ante
            ipsum primis in faucibus orci luctus et ultrices posuere cubilia
            curae;
          </p>
          <ul>
            <li>Quisque ullamcorper elit ut facilisis iaculis.</li>
            <li>
              Duis rutrum mauris nec felis imperdiet, a vulputate enim maximus.
            </li>
            <li>Sed nec urna eleifend, suscipit justo vel, facilisis nisl.</li>
          </ul>
        </>
      ),
    },
  ];

  const activeMapData = data.find((m) => m.id === activeMap);

  return (
    <Container style={{ padding: "16px" }}>
      <h1>Mapas del evento</h1>
      <h4>{event?.name}</h4>
      <div className="d-flex justify-content-center">
        <ButtonGroup aria-label="Basic example">
          <Button
            variant={activeMap == 1 ? "primary" : "outline-primary"}
            onClick={() => setActiveMap(1)}
          >
            Mapa 1
          </Button>
          <Button
            variant={activeMap == 2 ? "primary" : "outline-primary"}
            onClick={() => setActiveMap(2)}
          >
            Mapa 2
          </Button>
          <Button
            variant={activeMap == 3 ? "primary" : "outline-primary"}
            onClick={() => setActiveMap(3)}
          >
            Mapa 3
          </Button>
        </ButtonGroup>
      </div>
      <SwitchTransition>
        <CSSTransition
          key={activeMap}
          classNames="fade"
          timeout={200}
        >
          <Row style={{ paddingTop: "32px" }}>
            <Col md={activeMapData?.description ? 6 : 12}>
              <Image fluid src={activeMapData.image} />
            </Col>
            {activeMapData?.description && (
              <Col md={6}>
                <h5>Indicaciones:</h5>
                {activeMapData.description}
              </Col>
            )}
          </Row>
        </CSSTransition>
      </SwitchTransition>
    </Container>
  );
}
