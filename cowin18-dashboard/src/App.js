import React from "react";
import cowin18 from "./api/cowin18";
import CentersTable from "./CentersTable";

class App extends React.Component {
  state = {
    centers: [],
    selectedDistrict: "",
  };

  async componentDidMount() {
    const resp = await cowin18.get("/centers/");
    const centers = resp.data;
    this.setState({ centers, selectedDistrict: "DISTRICT_571" });
  }

  render() {
    return (
      <CentersTable
        data={this.state.centers?.[this.state.selectedDistrict] ?? []}
      />
    );
  }
}

export default App;
