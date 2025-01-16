import { Typography, Box, useTheme } from "@mui/material";
import { tokens } from "../hooks/useTheme";

const Header = ({ title, subtitle }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box mb="30px">
      <Typography
        variant="h2"
        color={colors.grey[100]}
        fontWeight="bold"
        sx={{ m: "5px 0 5px 20px" }}
      >
        {title}
      </Typography>
      <Typography variant="h5" color={colors.greenAccent[400]} sx={{m: "5px 0 5px 20px"}}>
        {subtitle}
      </Typography>
    </Box>
  );
};

export default Header;