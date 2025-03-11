import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { Alert, Button, Card, Form as BootstrapForm, Spinner } from 'react-bootstrap';

const validationSchema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email').required('Email is required'),
  phone: Yup.string().required('Phone number is required'),
  cv: Yup.mixed().required('CV is required'),
  status: Yup.string().required('Status is required')
});

const ApplicationForm = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState(null);

  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleSubmit = async (values, { resetForm }) => {
    setIsSubmitting(true);
    setSubmitResult(null);

    try {
      const formData = new FormData();
      formData.append('name', values.name);
      formData.append('email', values.email);
      formData.append('phone', values.phone);
      formData.append('cv', values.cv);
      formData.append('status', values.status);

      const response = await axios.post(`${apiUrl}/api/applications`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setSubmitResult({
        success: true,
        message: 'Application submitted successfully!',
        data: response.data
      });

      resetForm();
    } catch (error) {
      setSubmitResult({
        success: false,
        message: `Error: ${error.response?.data?.error || error.message}`
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="shadow-sm">
      <Card.Body className="p-4">
        <Formik
          initialValues={{
            name: '',
            email: '',
            phone: '',
            cv: null,
            status: 'testing'
          }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ errors, touched, setFieldValue }) => (
            <Form>
              <div className="mb-3">
                <label htmlFor="name" className="form-label">Name</label>
                <Field
                  name="name"
                  type="text"
                  className={`form-control ${errors.name && touched.name ? 'is-invalid' : ''}`}
                />
                <ErrorMessage name="name" component="div" className="invalid-feedback" />
              </div>

              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <Field
                  name="email"
                  type="email"
                  className={`form-control ${errors.email && touched.email ? 'is-invalid' : ''}`}
                />
                <ErrorMessage name="email" component="div" className="invalid-feedback" />
              </div>

              <div className="mb-3">
                <label htmlFor="phone" className="form-label">Phone Number</label>
                <Field
                  name="phone"
                  type="text"
                  className={`form-control ${errors.phone && touched.phone ? 'is-invalid' : ''}`}
                />
                <ErrorMessage name="phone" component="div" className="invalid-feedback" />
              </div>

              <div className="mb-3">
                <label htmlFor="cv" className="form-label">CV Upload (PDF or DOCX)</label>
                <BootstrapForm.Control
                  type="file"
                  name="cv"
                  accept=".pdf,.docx"
                  onChange={(event) => {
                    setFieldValue('cv', event.currentTarget.files[0]);
                  }}
                  isInvalid={errors.cv && touched.cv}
                />
                <ErrorMessage name="cv" component="div" className="invalid-feedback" />
              </div>

              <div className="mb-4">
                <label htmlFor="status" className="form-label">Submission Type</label>
                <Field name="status" as="select" className="form-select">
                  <option value="testing">Testing (Development)</option>
                  <option value="prod">Production (Final Submission)</option>
                </Field>
              </div>

              <Button type="submit" variant="primary" className="w-100" disabled={isSubmitting}>
                {isSubmitting ? (
                  <>
                    <Spinner animation="border" size="sm" className="me-2" />
                    Submitting...
                  </>
                ) : (
                  'Submit Application'
                )}
              </Button>
            </Form>
          )}
        </Formik>

        {submitResult && (
          <Alert
            variant={submitResult.success ? 'success' : 'danger'}
            className="mt-4"
          >
            {submitResult.message}
            {submitResult.success && submitResult.data && (
              <div className="mt-2">
                <p>Your CV is available at: <a href={submitResult.data.cv_url} target="_blank" rel="noreferrer">View CV</a></p>
              </div>
            )}
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
};

export default ApplicationForm;