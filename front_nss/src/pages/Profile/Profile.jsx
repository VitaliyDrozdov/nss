import { Box } from "@mui/material";
import Header from "../../components/Header";
import EditProfileForm from "./EditProfileForm";

const Profile = ()  => {

  return (
    <Box m="20px">
      <Header title="Профиль" subtitle="Изменение настроек" />

      <EditProfileForm />
    </Box>
  );
};

export default Profile;