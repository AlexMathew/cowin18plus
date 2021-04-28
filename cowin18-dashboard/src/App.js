import React from "react";
import cowin18 from "./api/cowin18";

class App extends React.Component {
  state = {
    centers: {},
  };

  async componentDidMount() {
    const resp = await cowin18.get("/centers/");
    const centers = resp.data;
    this.setState({ centers });
  }

  render() {
    return <div>App.</div>;
  }
}

export default App;
