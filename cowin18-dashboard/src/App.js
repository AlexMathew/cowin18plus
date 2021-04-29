import React from "react";
import _ from "lodash";
import { withStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import MuiAlert from "@material-ui/lab/Alert";
import cowin18 from "./api/cowin18";
import CentersTable from "./CentersTable";

const styles = (theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
});

class App extends React.Component {
  state = {
    districts: [],
    districtsById: {},
    updated: {},
    centers: {},
    selectedDistrict: "",
    selectedDistrictName: "",
  };

  async componentDidMount() {
    const resp = await cowin18.get("/centers/");
    const centers = resp.data.centers;
    const updated = resp.data.updated;
    const districts = resp.data.districts;
    this.setState({
      districts,
      districtsById: _.keyBy(districts, "id"),
      updated,
      centers,
    });
  }

  handleDistrictSelection = (event) => {
    const districtId = event.target.value;
    this.setState({
      selectedDistrict: districtId,
      selectedDistrictName: this.state.districtsById?.[districtId]?.name,
    });
  };

  render() {
    const { classes } = this.props;
    const lastUpdated = this.state.selectedDistrict
      ? `${this.state.selectedDistrictName}: Last updated - ${
          this.state.updated?.[
            `DISTRICT_UPDATED_${this.state.selectedDistrict}`
          ] ?? "never"
        }`
      : "";

    return (
      <div>
        <MuiAlert elevation={2} variant="filled" severity="warning">
          The data here could be outdated. {lastUpdated}
        </MuiAlert>
        <FormControl className={classes.formControl}>
          <InputLabel id="city-selector-label">City</InputLabel>
          <Select
            labelId="city-selector-label"
            id="city-selector"
            value={this.state.selectedDistrict}
            onChange={this.handleDistrictSelection}
          >
            {this.state.districts.map((district) => (
              <MenuItem key={district.id} value={district.id}>
                {district.name}
              </MenuItem>
            ))}
          </Select>
          <FormHelperText>Select City</FormHelperText>
        </FormControl>
        <CentersTable
          data={
            this.state.centers?.[`DISTRICT_${this.state.selectedDistrict}`] ??
            []
          }
        />
      </div>
    );
  }
}

export default withStyles(styles)(App);
