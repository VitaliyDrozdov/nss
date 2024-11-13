import React, { useContext } from "react";
import { Link } from 'react-router-dom';

import { Box, Button, IconButton, TextField, useTheme } from "@mui/material";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";

import { Formik } from "formik";
import * as yup from "yup";

import { ColorModeContext } from "../../hooks/useTheme";

const SignUpForm = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const handleFormSubmit = (values) => {
    console.log(values);
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
            display="grid"
            gap={3}
            gridTemplateColumns="repeat(4, minmax(0, 1fr))"
          >
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Имя"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.firstName}
              name="firstName"
              error={!!touched.firstName && !!errors.firstName}
              helperText={touched.firstName && errors.firstName}
              sx={{ gridColumn: "span 2" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Фамилия"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.lastName}
              name="lastName"
              error={!!touched.lastName && !!errors.lastName}
              helperText={touched.lastName && errors.lastName}
              sx={{ gridColumn: "span 2" }}
            />
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
              sx={{ gridColumn: "span 4" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Номер телефона"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.contact}
              name="contact"
              error={!!touched.contact && !!errors.contact}
              helperText={touched.contact && errors.contact}
              sx={{ gridColumn: "span 4" }}
            />
            <TextField
              fullWidth
              variant="filled"
              type="text"
              label="Должность"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.address2}
              name="position"
              error={!!touched.position && !!errors.position}
              helperText={touched.position && errors.position}
              sx={{ gridColumn: "span 4" }}
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
              <Button component={Link} to="/signin" color="warning" variant="contained" sx={{mr: 2}}>
                Войти
              </Button>
              <Button type="submit" color="secondary" variant="contained">
                Создать
              </Button>
            </Box>
          </Box>
        </form>
      )}
    </Formik>
  );
};

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/;

const checkoutSchema = yup.object().shape({
  firstName:  yup.string().required("обязательное!"),
  lastName:   yup.string().required("обязательное!"),
  email:      yup.string().email("invalid email").required("обязательное!"),
  contact: yup
    .string()
    .matches(phoneRegExp, "Phone number is not valid")
    .required("обязательное!"),
  position:   yup.string().required("обязательное!"),
});

const initialValues = {
  firstName: "",
  lastName: "",
  email: "",
  contact: "",
  position: "",
};

export default SignUpForm;
