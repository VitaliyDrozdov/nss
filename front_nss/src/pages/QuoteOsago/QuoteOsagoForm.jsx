import React from 'react';
import { TextField, Button, Box, Select, MenuItem, InputLabel, FormControl, Modal, Typography, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';

import { Formik, Form, FieldArray, Field } from 'formik';
import * as Yup from 'yup';
import api from "../../utils/api";



const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 600,
  height: 150,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const initialValues = {
  quote: {
    header: {
      runId: 'id',
      quoteId: 'id',
      dateTime: new Date().toISOString(),
    },
    product: {
      productType: 'osago',
      productCode: 'prod001',
    },
    subjects: [
      {
        firstName: '',
        secondName: '',
        middleName: '',
        birthDate: '',
        gender: '',
        addresses: [
          {
            country: '',
            region: '',
            city: '',
            street: '',
            houseNumber: '',
            apartmentNumber: '',
          },
        ],
        documents: [
          {
            documentType: 'passport',
            documentNumber: '',
            issueDate: '',
          },
        ],
      },
    ],
  },
};



const MuiTextField = ({ field, form, ...props }) => {
  return <TextField {...field} {...props} />;
};



const Page = () => {
  const [IsOpen, setOpen] = React.useState(false);
  const [data, setData] = React.useState({
    "predict": {
      "percent": "undefined",
      "score": 0
    }
  });
  const [IsOpenError, setOpenError] = React.useState(false);
  const [error_message, setErrorMessage] = React.useState("");
  const handleOpen = (data) => {
    setData(data)
    setOpen(true)

  };
  const handleClose = () => setOpen(false);
  const handleCloseError = () => setOpenError(false);
  const handleOpenError = (error) => {
    setErrorMessage(error)
    setOpenError(true)
  };

  const checkoutSchema = Yup.object().shape({
    quote: Yup.object().shape({
      header: Yup.object().shape({
        runId: Yup.string().required('Run ID обязательное поле'),
        quoteId: Yup.string().required('Quote ID обязательное поле'),
      }),
      subjects: Yup.array().of(
        Yup.object().shape({
          firstName: Yup.string().required('Имя обязательно!'),
          secondName: Yup.string().required('Фамилия обязательна!'),
          middleName: Yup.string(),
          birthDate: Yup.date().required('Дата рождения обязательна!'),
          gender: Yup.string().required('Пол обязателен!'),
          addresses: Yup.array().of(
            Yup.object().shape({
              country: Yup.string().required('Страна адреса обязательна!'),
              region: Yup.string().required('Регион обязателен!'),
              city: Yup.string().required('Город обязателен!'),
              street: Yup.string().required('Улица обязательна!'),
              houseNumber: Yup.string().required('Номер дома обязателен!'),
              apartmentNumber: Yup.string(),
            })
          ),
          documents: Yup.array().of(
            Yup.object().shape({
              documentType: Yup.string().required('Обязательно указать тип документа'),
              documentNumber: Yup.string().required('Номер документа обязателен!'),
              issueDate: Yup.date().required('Срок действия документа обязателен!'),
            })
          ),
        })
      ),
    }),
  });

  const handleSubmit = async (values) => {
  try {
    const response = await api.post('/quote', values);

    if (response.status === 200) {
      handleOpen(response.data)
    }
  } catch (error) {
    handleOpenError((error.response.data.detals ?? "Ошибка") + ": " + error.response.data.error)
  }
  };



  return (
    <Box m="20px">
      <Modal
        open={IsOpen}
        onClose={handleClose}
      >
        <Box sx={style}>
          <Typography id="Modal-quote" variant="h6" component="h2">
            Предсказание
          </Typography>
          <Typography id="modal-quote-details" sx={{ mt: 2 }}>
            <p>Predict Percent: {data.predict.percent}</p>
            <p>Predict Score: {data.predict.score}</p>

          </Typography>

          <Button onClick={handleClose} color="secondary">Close</Button>
        </Box>
      </Modal>

      <Modal
        open={IsOpenError}
        onClose={handleCloseError}>
        <Box sx={style} display={"grid"}>
          <Typography variant='h5' marginBottom={"auto"}>{error_message}</Typography>

          <Button onClick={handleCloseError} color="secondary" >Close</Button>
        </Box>
      </Modal>

      <Formik
        initialValues={initialValues}
        onSubmit={handleSubmit}
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

          <Form onSubmit={handleSubmit}>

            <Field
              name="quote.header.runId"
              placeholder="Run ID"
              component={MuiTextField}
              onBlur={handleBlur}
              onChange={handleChange}
              error={!!touched.quote?.header?.runId && !!errors.quote?.header?.runId}
              helperText={touched.quote?.header?.runId && errors.quote?.header?.runId}

            />

            <Field
              name="quote.header.quoteId"
              placeholder="Quote ID"
              component={MuiTextField}
              onChange={handleChange}
              onBlur={handleBlur}
              error={!!touched.quote?.header?.quoteId && !!errors.quote?.header?.quoteId}
              helperText={touched.quote?.header?.quoteId && errors.quote?.header?.quoteId}
            />

            <FieldArray name="quote.subjects">
              {({ push, remove }) => (
                <div>
                  {values.quote.subjects.map((subject, index) => (
                    <div key={index}>
                      <h3>Subject {index + 1}</h3>

                      <Field
                        name={`quote.subjects.${index}.secondName`}
                        placeholder="Фамилия"
                        component={MuiTextField}
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.quote.subjects[index].secondName}
                        error={!!touched.quote?.subjects?.[index]?.secondName && !!errors.quote?.subjects?.[index]?.secondName}
                        helperText={touched.quote?.subjects?.[index]?.secondName && errors.quote?.subjects?.[index]?.secondName}
                      />

                      <Field
                        name={`quote.subjects.${index}.firstName`}
                        placeholder="Имя"
                        component={MuiTextField}
                        onChange={handleChange}
                        error={!!touched.quote?.subjects?.[index]?.firstName && !!errors.quote?.subjects?.[index]?.firstName}
                        helperText={touched.quote?.subjects?.[index]?.firstName && errors.quote?.subjects?.[index]?.firstName}
                      />

                      <Field
                        name={`quote.subjects.${index}.middleName`}
                        placeholder="Отчество"
                        component={MuiTextField}
                      />


                      <Field
                        name={`quote.subjects.${index}.birthDate`}
                        type="date"
                        component={MuiTextField}
                        error={!!touched.quote?.subjects?.[index]?.birthDate && !!errors.quote?.subjects?.[index]?.birthDate}
                        helperText={touched.quote?.subjects?.[index]?.birthDate && errors.quote?.subjects?.[index]?.birthDate}
                      />


                      <FormControl variant="filled" sx={{ m: 1, minWidth: 120 }}>
                        <InputLabel>Gender</InputLabel>
                        <Field
                          as={Select}
                          name={`quote.subjects.${index}.gender`}
                          label="Gender"
                          error={!!touched.quote?.subjects?.[index]?.gender && !!errors.quote?.subjects?.[index]?.gender}
                          helperText={touched.quote?.subjects?.[index]?.gender && errors.quote?.subjects?.[index]?.gender}
                        >
                          <MenuItem value="male">Male</MenuItem>
                          <MenuItem value="female">Female</MenuItem>
                        </Field>
                      </FormControl>

                      <FieldArray name={`quote.subjects.${index}.addresses`}>
                        {({ push: pushAddress, remove: removeAddress }) => (
                          <div>
                            {subject.addresses.map((address, addressIndex) => (
                              <div key={addressIndex}>
                                <h4>Address {addressIndex + 1}</h4>
                                <Field
                                  name={`quote.subjects.${index}.addresses.${addressIndex}.country`}
                                  placeholder="Country"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.country && !!errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.country}
                                  helperText={touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.country && errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.country}
                                />

                                <Field
                                  name={`quote.subjects.${index}.addresses.${addressIndex}.region`}
                                  placeholder="Region"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.region && !!errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.region}
                                  helperText={touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.region && errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.region}
                                />

                                <Field
                                  name={`quote.subjects.${index}.addresses.${addressIndex}.city`}
                                  placeholder="City"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.city && !!errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.city}
                                  helperText={touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.city && errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.city}
                                />

                                <Field
                                  name={`quote.subjects.${index}.addresses.${addressIndex}.street`}
                                  placeholder="Street"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.street && !!errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.street}
                                  helperText={touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.street && errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.street}
                                />

                                <Field
                                  name={`quote.subjects.${index}.addresses.${addressIndex}.houseNumber`}
                                  placeholder="House Number"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.houseNumber && !!errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.houseNumber}
                                  helperText={touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.houseNumber && errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.houseNumber}
                                />

                                <Field
                                  name={`quote.subjects.${index}.addresses.${addressIndex}.apartmentNumber`}
                                  placeholder="Apartment Number"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.apartmentNumber && !!errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.apartmentNumber}
                                  helperText={touched.quote?.subjects?.[index]?.addresses?.[addressIndex]?.apartmentNumber && errors.quote?.subjects?.[index]?.addresses?.[addressIndex]?.apartmentNumber}
                                />

                                <Box >
                                  <Button type="button" color="removing" variant="contained" onClick={() => removeAddress(addressIndex)}>Remove Address</Button>
                                </Box>
                              </div>
                            ))}
                            <Box
                              display="grid"
                              gap="70px"
                              gridTemplateColumns="repeat(6, minmax(0, 1fr))"
                            >
                              <Button type="button" color="secondary" variant="contained" sx={{ mt: 2 }} onClick={() => pushAddress({ country: '', region: '', city: '', street: '', houseNumber: '', apartmentNumber: '' })}>
                                Add Another Address
                              </Button>
                            </Box>
                          </div>
                        )}
                      </FieldArray>

                      <FieldArray name={`quote.subjects.${index}.documents`}>
                        {({ push: pushDocument, remove: removeDocument }) => (
                          <div>
                            {subject.documents.map((document, documentIndex) => (
                              <div key={documentIndex}>
                                <h4>Document {documentIndex + 1}</h4>
                                <Field
                                  name={`quote.subjects.${index}.documents.${documentIndex}.documentType`}
                                  placeholder="Document Type"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentType && !!errors.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentType}
                                  helperText={touched.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentType && errors.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentType}
                                />

                                <Field
                                  name={`quote.subjects.${index}.documents.${documentIndex}.documentNumber`}
                                  placeholder="Document Number"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentNumber && !!errors.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentNumber}
                                  helperText={touched.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentNumber && errors.quote?.subjects?.[index]?.documents?.[documentIndex]?.documentNumber}
                                />

                                <Field
                                  name={`quote.subjects.${index}.documents.${documentIndex}.issueDate`}
                                  type="date"
                                  component={MuiTextField}
                                  error={!!touched.quote?.subjects?.[index]?.documents?.[documentIndex]?.issueDate && !!errors.quote?.subjects?.[index]?.documents?.[documentIndex]?.issueDate}
                                  helperText={touched.quote?.subjects?.[index]?.documents?.[documentIndex]?.issueDate && errors.quote?.subjects?.[index]?.documents?.[documentIndex]?.issueDate}
                                />

                                <Box>
                                  <Button type="button" color="removing" variant="contained" onClick={() => removeDocument(documentIndex)}>Remove Document</Button>
                                </Box>
                              </div>
                            ))}
                            <Box
                              display="grid"
                              gap="70px"
                              gridTemplateColumns="repeat(6, minmax(0, 1fr))"
                              mt={2}
                            >
                              <Button type="button" color="secondary" variant="contained" justifyContent="space-between" onClick={() => pushDocument({ documentType: '', documentNumber: '', issueDate: '' })}>
                                Add Another Document
                              </Button>
                            </Box>
                          </div>
                        )}
                      </FieldArray>
                      <Box

                        mt={2}
                      >
                        <Button type="button" color="removing" variant="contained" onClick={() => remove(index)}>Remove Subject</Button>
                      </Box>
                    </div>
                  ))}
                  <Box
                    display="grid"
                    gap="70px"
                    gridTemplateColumns="repeat(6, minmax(0, 1fr))"
                    mt={2}
                  >
                    <Button
                      type="button"
                      color="secondary"
                      variant="contained"
                      onClick={() => push({
                        firstName: '',
                        secondName: '',
                        middleName: '',
                        birthDate: '',
                        gender: '',
                        addresses: [],
                        documents: []
                      })}>
                      Add Subject
                    </Button>
                  </Box>
                </div>
              )}
            </FieldArray>

            <Box
              display="grid"
              gap="70px"
              gridTemplateColumns="repeat(3, minmax(0, 1fr))"
              mt={2}
            >


              <Button type="submit" color="third" variant="contained" onClick={handleSubmit}>
                Submit
              </Button>
            </Box>

          </Form>
        )}
      </Formik>

    </Box>
  );

};

export default Page;