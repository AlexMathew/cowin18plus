import React from "react";
import _ from "lodash";
import { withStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import MuiAlert from "@material-ui/lab/Alert";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import cowin18 from "./api/cowin18";
import CentersTable from "./CentersTable";

const styles = (theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: theme.spacing(40),
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: "white",
  },
});

class App extends React.Component {
  state = {
    loading: false,
    states: [],
    districts: {},
    selectedState: "",
    selectedDistrict: "",
    centers: {},
    updated: {},
  };

  async componentDidMount() {
    try {
      this.setState({ loading: true });
      const resp = await cowin18.get("/districts/");
      const states = resp.data.states;
      const districts = resp.data.districts;
      this.setState({
        states,
        districts,
      });
    } catch (error) {
      console.log(error);
    } finally {
      this.setState({ loading: false });
    }
    const urlParams = new URLSearchParams(window.location.search);
    const state = urlParams.get("state");
    // const district = urlParams.get("district");
    if (state) {
      const statesByName = _.keyBy(this.state.states, "state_name");
      const preselectedState = statesByName?.[state];
      if (preselectedState) {
        this.selectState(preselectedState.state_id);
      }
    }
  }

  selectState = async (stateId) => {
    this.setState({
      selectedState: stateId,
      selectedDistrict: "",
    });
    if (!Object.keys(this.state.centers).includes(stateId.toString())) {
      try {
        this.setState({ loading: true });
        const resp = await cowin18.get("/centers/", { params: { stateId } });
        const updated = resp.data.updated;
        const centers = resp.data.centers;
        this.setState({
          centers: { ...this.state.centers, [stateId]: centers },
          updated: { ...this.state.updated, [stateId]: updated },
        });
      } catch (error) {
        console.log(error);
      } finally {
        this.setState({ loading: false });
      }
    }
  };

  selectDistrict = (districtId) => {
    this.setState({
      selectedDistrict: districtId,
    });
  };

  handleStateSelection = (event) => {
    const stateId = event.target.value;
    this.selectState(stateId);
  };

  handleDistrictSelection = (event) => {
    const districtId = event.target.value;
    this.selectDistrict(districtId);
  };

  getLastUpdatedText = () => {
    const districts = this.state.districts?.[this.state.selectedState];
    if (!districts) return "";
    const districtsById = _.keyBy(districts, "district_id");
    const selectedDistrictName =
      districtsById?.[this.state.selectedDistrict]?.district_name ?? "";
    return this.state.selectedDistrict
      ? `${selectedDistrictName}: Last updated - ${
          this.state.updated?.[this.state.selectedState]?.[
            `DISTRICT_UPDATED_${this.state.selectedDistrict}`
          ] ?? "never"
        }`
      : "";
  };

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Backdrop className={classes.backdrop} open={this.state.loading}>
          <CircularProgress color="inherit" />
        </Backdrop>
        <MuiAlert elevation={2} variant="filled" severity="warning">
          The data here could be outdated. {this.getLastUpdatedText()}
        </MuiAlert>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel id="state-selector-label">State</InputLabel>
          <Select
            labelId="state-selector-label"
            id="state-selector"
            value={this.state.selectedState}
            onChange={this.handleStateSelection}
          >
            {this.state.states.map((state) => (
              <MenuItem key={state.state_id} value={state.state_id}>
                {state.state_name}
              </MenuItem>
            ))}
          </Select>
          <FormHelperText>Select State</FormHelperText>
        </FormControl>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel id="district-selector-label">District</InputLabel>
          <Select
            labelId="district-selector-label"
            id="district-selector"
            value={this.state.selectedDistrict}
            onChange={this.handleDistrictSelection}
          >
            {(this.state.districts?.[this.state.selectedState] ?? []).map(
              (district) => (
                <MenuItem
                  key={district.district_id}
                  value={district.district_id}
                >
                  {district.district_name}
                </MenuItem>
              )
            )}
          </Select>
          <FormHelperText>Select District</FormHelperText>
        </FormControl>
        <CentersTable
          data={
            this.state.centers?.[this.state.selectedState]?.[
              `DISTRICT_${this.state.selectedDistrict}`
            ] ?? []
          }
        />
      </div>
    );
  }
}

export default withStyles(styles)(App);
