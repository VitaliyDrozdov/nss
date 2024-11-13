import React, { useContext } from "react";
import { Link, useNavigate } from 'react-router-dom';

import { Box, Button, IconButton, TextField, useTheme } from "@mui/material";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";

import { Formik } from "formik";
import * as yup from "yup";

import { ColorModeContext } from "../../hooks/useTheme";
import { useAuth } from "../../hooks/useAuth"; 

const SignInForm = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const  { login } = useAuth();
  const navigate = useNavigate();

  const handleFormSubmit = (values) => {
    console.log(values);

    login();
    navigate("/test");
  };

  return (
    <Formik
      onSubmit={handleFormSubmit}
      initialValues={initialValues}
      validationSchema={checkoutSchema}
    >
      {({
        values,
        errors,
        touched,
        handleBlur,
        handleChange,
        handleSubmit,
      }) => (
        <form onSubmit={handleSubmit}>
          <Box
            display="flex"
            flexDirection="column"
            minWidth="420px"
            gap={3}
          >
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Email"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.email}
              name="email"
              error={!!touched.email && !!errors.email}
              helperText={touched.email && errors.email}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Пароль"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.contact}
              name="password"
              error={!!touched.password && !!errors.password}
              helperText={touched.password && errors.password}
            />
          </Box>
          <Box display="flex" justifyContent="space-between" mt={2}>
            <IconButton onClick={colorMode.toggleColorMode}>
              {theme.palette.mode === "dark" ? (
                <DarkModeOutlinedIcon />
              ) : (
                <LightModeOutlinedIcon />
              )}
            </IconButton>
            <Box>
              <Button component={Link} to="/signup" color="warning" variant="contained" sx={{mr: 2}}>
                Регистрация
              </Button>
              <Button type="submit" color="secondary" variant="contained">
                Войти
              </Button>
            </Box>
          </Box>
        </form>
      )}
    </Formik>
  );
};

const checkoutSchema = yup.object().shape({
  email:      yup.string().email("invalid email").required("обязательное!"),
  password:   yup.string().required("обязательное!"),
});

const initialValues = {
  email: "",
  password: "",
};

export default SignInForm;
