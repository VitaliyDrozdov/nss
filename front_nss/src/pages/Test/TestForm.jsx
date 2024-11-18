import React from 'react';
import { TextField, Button, Box, Select, MenuItem, InputLabel, FormControl, Modal, Typography } from '@mui/material';
import { Formik, Form, FieldArray, Field } from 'formik';
import * as Yup from 'yup';

//адрес вашего эндпоинта, который будет принимать запросы из формы
const address = 'http://localhost:5000/api/quote';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 600,
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
      productCode: '0',
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
  const[IsOpenError, setOpenError] = React.useState(false);
  const [error_message, setErrorMessage] = React.useState("");
  const handleOpen = (data) => {
    setData(data)
    setOpen(true)

  };
  const handleClose = () => setOpen(false);
  const handleCloseError = () => setOpenError(false);
  const handleOpenError = (error) => {
    setErrorMessage(error)
    setOpenError(true)};



  const handleSubmit = (values) => {
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(values)
    }

    fetch(address, params)
      .then(response => {
          if (response.status === 400) {
              throw new Error("Необходимо заполнить все поля формы для получения предсказания");
          }
          else if (response.status === 500) {
            throw new Error("Сервер недоступен");
          }
        console.log("start parsing data")
        return response.json()
      })
      .then(data => {
        handleOpen(data)
        return data;
      })
      .catch(error => {
        handleOpenError(error.message)
      });
  };

  return (
    <>
      <Modal
        open={IsOpen}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description">
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Предсказание
          </Typography>
          <Typography id="modal-modal-description" sx={{ mt: 2 }}>
            <p>Predict Percent: {data.predict.percent}</p>
            <p>Predict Score: {data.predict.score}</p>

          </Typography>

          <Button onClick={handleClose} color="secondary">Close</Button>
        </Box>
      </Modal>

      <Modal
        open={IsOpenError}
        onClose={handleCloseError}>
        <Box sx={style}>
          <p>{error_message}</p>
        <Button onClick={handleCloseError} color="secondary">Close</Button>
        </Box>
      </Modal>




      <Formik
        initialValues={initialValues}
        onSubmit={handleSubmit}
      >

        {({ values }) => (

          <Form>
            <Field name="quote.header.runId" placeholder="Run ID" component={MuiTextField} />


            <Field name="quote.header.quoteId" placeholder="Quote ID" component={MuiTextField} />

            <FieldArray name="quote.subjects">
              {({ push, remove }) => (
                <div>
                  {values.quote.subjects.map((subject, index) => (
                    <div key={index}>
                      <h3>Subject {index + 1}</h3>
                      <Field name={`quote.subjects.${index}.firstName`} placeholder="First Name" component={MuiTextField} />

                      <Field name={`quote.subjects.${index}.secondName`} placeholder="Second Name" component={MuiTextField} />

                      <Field name={`quote.subjects.${index}.middleName`} placeholder="Middle Name" component={MuiTextField} />


                      <Field name={`quote.subjects.${index}.birthDate`} type="date" component={MuiTextField} />


                      <FormControl variant="filled" sx={{ m: 1, minWidth: 120 }}>
                        <InputLabel>Gender</InputLabel>
                        <Field as={Select} name={`quote.subjects.${index}.gender`} label="Gender">
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
                                <Field name={`quote.subjects.${index}.addresses.${addressIndex}.country`} placeholder="Country" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.addresses.${addressIndex}.region`} placeholder="Region" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.addresses.${addressIndex}.city`} placeholder="City" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.addresses.${addressIndex}.street`} placeholder="Street" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.addresses.${addressIndex}.houseNumber`} placeholder="House Number" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.addresses.${addressIndex}.apartmentNumber`} placeholder="Apartment Number" component={MuiTextField} />
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
                                <Field name={`quote.subjects.${index}.documents.${documentIndex}.documentType`} placeholder="Document Type" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.documents.${documentIndex}.documentNumber`} placeholder="Document Number" component={MuiTextField} />
                                <Field name={`quote.subjects.${index}.documents.${documentIndex}.issueDate`} type="date" component={MuiTextField} />
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


              <Button type="submit" color="third" variant="contained" >
                Submit
              </Button>
            </Box>

          </Form>
        )}
      </Formik>

    </>
  );


};




export default Page;