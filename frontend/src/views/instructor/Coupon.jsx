import { useState, useEffect } from "react";
import moment from "moment";

import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

import Sidebar from "./Partials/Sidebar";
import Header from "./Partials/Header";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";

import useAxios from "../../utils/useAxios";
import Useta from "../plugin/UserData";
import { teacherId } from "../../utils/constants";
import UserData from "../plugin/UserData";
import Toast from "../plugin/Toast";

function Coupon() {
  const [coupons, setCoupons] = useState([]);
  const [createCoupon, setCreateCoupon] = useState({ code: "", discount: 0 });
  const [selectedCoupon, setSelectedCoupon] = useState([]);

  const [show, setShow] = useState(false);
  const [showAddCoupon, setShowAddCoupon] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = (coupon) => {
    setShow(true);
    setSelectedCoupon(coupon);
  };

  const handleAddCouponClose = () => setShowAddCoupon(false);
  const handleAddCouponShow = () => setShowAddCoupon(true);

  const fetchCoupons = () => {
    useAxios()
      .get(`teacher/coupon-list/${UserData()?.teacher_id}/`)
      .then((res) => {
        console.log(res.data);
        setCoupons(res.data);
      });
  };

  useEffect(() => {
    fetchCoupons();
  }, []);

  const handleCreateCouponChange = (event) => {
    setCreateCoupon({
      ...createCoupon,
      [event.target.name]: event.target.value,
    });
  };

  const handleCouponSubmit = (e) => {
    e.preventDefault();

    const formdata = new FormData();

    formdata.append("teacher", UserData()?.teacher_id);
    formdata.append("code", createCoupon.code);
    formdata.append("discount", createCoupon.discount);

    useAxios()
      .post(`teacher/coupon-list/${UserData()?.teacher_id}/`, formdata)
      .then((res) => {
        console.log(res.data);
        fetchCoupons();
        handleAddCouponClose();
        Toast().fire({
          icon: "success",
          title: "Coupon created successfully",
        });
      });
  };

  const handleDeleteCoupon = (couponId) => {
    useAxios()
      .delete(`teacher/coupon-detail/${UserData()?.teacher_id}/${couponId}/`)
      .then((res) => {
        console.log(res.data);
        fetchCoupons();
        Toast().fire({
          icon: "success",
          title: "Coupon deleted successfully",
        });
      });
  };

  const handleCouponUpdateSubmit = (e) => {
    e.preventDefault();

    const formdata = new FormData();

    formdata.append("teacher", UserData()?.teacher_id);
    formdata.append("code", createCoupon.code);
    formdata.append("discount", createCoupon.discount);

    useAxios()
      .patch(
        `teacher/coupon-detail/${UserData()?.teacher_id}/${selectedCoupon.id}/`,
        formdata
      )
      .then((res) => {
        console.log(res.data);
        fetchCoupons();
        handleClose();
        Toast().fire({
          icon: "success",
          title: "Coupon updated successfully",
        });
      });
  };

  return (
    <>
      <BaseHeader />

      <section className="pt-5 pb-5">
        <div className="container">
          {/* Header Here */}
          <Header />
          <div className="row mt-0 mt-md-4">
            {/* Sidebar Here */}
            <Sidebar />
            <div className="col-lg-9 col-md-8 col-12">
              {/* Card */}
              <div className="card mb-4">
                {/* Card header */}
                <div className="card-header d-lg-flex align-items-center justify-content-between">
                  <div className="mb-3 mb-lg-0">
                    <h3 className="mb-0">Coupons</h3>
                    <span>Manage all your coupons from here</span>
                  </div>
                  <button
                    className="btn btn-primary"
                    onClick={handleAddCouponShow}
                  >
                    Add Coupon
                  </button>
                </div>
                {/* Card body */}
                <div className="card-body">
                  {/* List group */}
                  <ul className="list-group list-group-flush">
                    {/* List group item */}
                    {coupons?.map((c, index) => (
                      <li className="list-group-item p-4 shadow rounded-3 mb-3">
                        <div className="d-flex">
                          <div className="ms-3 mt-2">
                            <div className="d-flex align-items-center justify-content-between">
                              <div>
                                <h4 className="mb-0">{c.code}</h4>
                                <span>{c.used_by} Student</span>
                              </div>
                            </div>
                            <div className="mt-2">
                              <p className="mt-2">
                                <span className="me-2 fw-bold">
                                  Discount:{" "}
                                  <span className="fw-light">
                                    {c.discount}% Discount
                                  </span>
                                </span>
                              </p>
                              <p className="mt-1">
                                <span className="me-2 fw-bold">
                                  Date Created:{" "}
                                  <span className="fw-light">
                                    {moment(c.date).format("DD MMM, YYYY")}
                                  </span>
                                </span>
                              </p>
                              <p>
                                <button
                                  class="btn btn-outline-secondary"
                                  type="button"
                                  onClick={() => handleShow(c)}
                                >
                                  Update Coupon
                                </button>

                                <button
                                  class="btn btn-danger ms-2"
                                  type="button"
                                  onClick={() => handleDeleteCoupon(c.id)}
                                >
                                  <i className="fas fa-trash"></i>
                                </button>
                              </p>
                            </div>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>
            Update Coupon -{" "}
            <span className="fw-bold">{selectedCoupon.code}</span>
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form onSubmit={handleCouponUpdateSubmit}>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">
                Code
              </label>
              <input
                type="text"
                placeholder="Code"
                defaultValue={selectedCoupon.code}
                className="form-control"
                name="code"
                onChange={handleCreateCouponChange}
              />
              <label for="exampleInputEmail1" class="form-label mt-3">
                Discount
              </label>
              <input
                type="text"
                placeholder="Discount"
                defaultValue={selectedCoupon.discount}
                className="form-control"
                name="discount"
                onChange={handleCreateCouponChange}
                id=""
              />
            </div>

            <button type="submit" class="btn btn-primary">
              Update Coupon <i className="fas fa-check-circle"> </i>
            </button>

            <Button className="ms-2" variant="secondary" onClick={handleClose}>
              Close
            </Button>
          </form>
        </Modal.Body>
      </Modal>

      <Modal show={showAddCoupon} onHide={handleAddCouponClose}>
        <Modal.Header closeButton>
          <Modal.Title>Create New Coupon</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form onSubmit={handleCouponSubmit}>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">
                Code
              </label>
              <input
                type="text"
                placeholder="Code"
                value={createCoupon.code}
                className="form-control"
                name="code"
                onChange={handleCreateCouponChange}
              />
              <label for="exampleInputEmail1" class="form-label mt-3">
                Discount
              </label>
              <input
                type="text"
                placeholder="Discount"
                value={createCoupon.discount}
                className="form-control"
                name="discount"
                onChange={handleCreateCouponChange}
                id=""
              />
            </div>

            <button type="submit" class="btn btn-primary">
              Create Coupon <i className="fas fa-plus"> </i>
            </button>

            <Button
              className="ms-2"
              variant="secondary"
              onClick={handleAddCouponClose}
            >
              Close
            </Button>
          </form>
        </Modal.Body>
      </Modal>

      <BaseFooter />
    </>
  );
}

export default Coupon;
