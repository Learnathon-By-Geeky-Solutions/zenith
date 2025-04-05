import { useState, useEffect } from "react";
import moment from "moment";

import Sidebar from "./Partials/Sidebar";
import Header from "./Partials/Header";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";

import useAxios from "../../utils/useAxios";
import UserData from "../plugin/UserData";
import { Link } from "react-router-dom";

function Courses() {
    const [courses, setCourses] = useState([]);

    const fetchCourseData = () => {
      useAxios()
        .get(`teacher/course-lists/${UserData()?.teacher_id}/`)
        .then((res) => {
          console.log(res.data);
          setCourses(res.data);
        });
    };

    useEffect(() => {
      fetchCourseData();
    }, []);

    const handleSearch = (event) => {
      const query = event.target.value.toLowerCase();
      console.log(query);
      if (query === "") {
        fetchCourseData();
      } else {
        const filtered = courses.filter((c) => {
          return c.title.toLowerCase().includes(query);
        });
        setCourses(filtered);
      }
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
              <div className="row mb-4">
                <h4 className="mb-0 mb-2 mt-4">
                  {" "}
                  <i className="bi bi-grid-fill"></i> Courses
                </h4>
              </div>
              <div className="card mb-4">
                <div className="card-header">
                  <h3 className="mb-0">Courses</h3>
                  <span>
                    Manage your courses from here, earch, view, edit or delete
                    courses.
                  </span>
                </div>
                <div className="card-body">
                  <form className="row gx-3">
                    <div className="col-lg-12 col-md-12 col-12 mb-lg-0 mb-2">
                      <input
                        type="search"
                        className="form-control"
                        placeholder="Search Your Courses"
                        onChange={handleSearch}
                      />
                    </div>
                  </form>
                </div>
                <div className="table-responsive overflow-y-hidden">
                  <table className="table mb-0 text-nowrap table-hover table-centered text-nowrap">
                    <thead className="table-light">
                      <tr>
                        <th>Courses</th>
                        <th>Enrolled</th>
                        <th>Level</th>
                        <th>Status</th>
                        <th>Date Created</th>
                        <th>Action</th>
                        <th />
                      </tr>
                    </thead>
                    <tbody>
                      {courses?.map((c, index) => (
                        <tr>
                          <td>
                            <div className="d-flex align-items-center">
                              <div>
                                <a href="#">
                                  <img
                                    src={c.image}
                                    alt="course"
                                    className="rounded img-4by3-lg"
                                    style={{
                                      width: "100px",
                                      height: "70px",
                                      borderRadius: "50%",
                                      objectFit: "cover",
                                    }}
                                  />
                                </a>
                              </div>
                              <div className="ms-3">
                                <h4 className="mb-1 h6">
                                  <a
                                    href="#"
                                    className="text-inherit text-decoration-none text-dark"
                                  >
                                    {c.title}
                                  </a>
                                </h4>
                                <ul className="list-inline fs-6 mb-0">
                                  <li className="list-inline-item">
                                    <small>
                                      <i className="fas fa-user"></i>
                                      <span className="ms-1">{c.language}</span>
                                    </small>
                                  </li>
                                  <li className="list-inline-item">
                                    <small>
                                      <i className="bi bi-reception-4"></i>
                                      <span className="ms-1">{c.level}</span>
                                    </small>
                                  </li>
                                  <li className="list-inline-item">
                                    <small>
                                      <i className="fas fa-dollar-sign"></i>
                                      <span>{c.price}</span>
                                    </small>
                                  </li>
                                </ul>
                              </div>
                            </div>
                          </td>
                          <td>
                            <p className="mt-3">{c.students?.length}</p>
                          </td>
                          <td>
                            <p className="mt-3 badge bg-success">{c.level}</p>
                          </td>
                          <td>
                            <p className="mt-3 badge bg-warning text-dark">
                              Intermediate
                            </p>
                          </td>
                          <td>
                            <p className="mt-3">
                              {moment(c.date).format("DD MMM, YYYY")}
                            </p>
                          </td>
                          <td>
                            <Link
                              to={`/instructor/edit-course/${c.course_id}/`}
                              className="btn btn-primary btn-sm mt-3 me-1"
                            >
                              <i className="fas fa-edit"></i>
                            </Link>
                            <button className="btn btn-danger btn-sm mt-3 me-1">
                              <i className="fas fa-trash"></i>
                            </button>
                            <button className="btn btn-secondary btn-sm mt-3 me-1">
                              <i className="fas fa-eye"></i>
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default Courses;
