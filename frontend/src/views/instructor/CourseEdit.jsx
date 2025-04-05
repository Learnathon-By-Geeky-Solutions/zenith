import { useState, useEffect } from "react";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

import Sidebar from "./Partials/Sidebar";
import Header from "./Partials/Header";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import { Link, useParams } from "react-router-dom";

import useAxios from "../../utils/useAxios";
import UserData from "../plugin/UserData";
import Swal from "sweetalert2";
import Toast from "../plugin/Toast";

function CourseEdit() {
  const [course, setCourse] = useState({
    category: 0,
    file: "",
    image: "",
    title: "",
    description: "",
    price: "",
    level: "",
    language: "",
    teacher_course_status: "",
  });

  const [category, setCategory] = useState([]);
  const [progress, setProgress] = useState(0);
  const [ckEdtitorData, setCKEditorData] = useState("");
  const param = useParams();
  const [variants, setVariants] = useState([
    {
      title: "",
      items: [{ title: "", description: "", file: "", preview: false }],
    },
  ]);

  const fetchCourseDetail = () => {
    useAxios()
      .get(`course/category/`)
      .then((res) => {
        setCategory(res.data);
      });

    useAxios()
      .get(`teacher/course-detail/${param.course_id}/`)
      .then((res) => {
        setCourse(res.data);
        setVariants(res.data.curriculum);
        setCKEditorData(res.data.description);
      });
  };

  useEffect(() => {
    fetchCourseDetail();
  }, []);
  console.log(course);

  const handleCourseInputChange = (event) => {
    setCourse({
      ...course,
      [event.target.name]:
        event.target.type === "checkbox"
          ? event.target.checked
          : event.target.value,
    });
  };

  const handleCkEditorChange = (event, editor) => {
    const data = editor.getData();
    setCKEditorData(data);
    console.log(ckEdtitorData);
  };

  const handleCourseImageChange = (event) => {
    const file = event.target.files[0];
    console.log(file);

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCourse({
          ...course,
          image: {
            file: event.target.files[0],
            preview: reader.result,
          },
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCourseIntroVideoChange = (event) => {
    setCourse({
      ...course,
      [event.target.name]: event.target.files[0],
    });
  };

  const handleVariantChange = (index, propertyName, value) => {
    const updatedVariants = [...variants];
    updatedVariants[index][propertyName] = value;
    setVariants(updatedVariants);

    console.log(`Name: ${propertyName} - value: ${value} - Index: ${index}`);
    console.log(variants);
  };

  const handleItemChange = (
    variantIndex,
    itemIndex,
    propertyName,
    value,
    type
  ) => {
    const updatedVariants = [...variants];
    updatedVariants[variantIndex].items[itemIndex][propertyName] = value;
    setVariants(updatedVariants);

    console.log(
      `Name: ${propertyName} - value: ${value} - Index: ${variantIndex} ItemIndex: ${itemIndex} - type: ${type}`
    );
  };

  const addVariant = () => {
    setVariants([
      ...variants,
      {
        title: "",
        items: [{ title: "", description: "", file: "", preview: false }],
      },
    ]);
  };

  const removeVariant = (index, variantId) => {
    const updatedVariants = [...variants];
    updatedVariants.splice(index, 1);
    setVariants(updatedVariants);

    useAxios()
      .delete(
        `teacher/course/variant-delete/${variantId}/${UserData()?.teacher_id}/${param.course_id}/`
      )
      .then((res) => {
        console.log(res.data);
        fetchCourseDetail();
        Toast().fire({
          icon: "success",
          title: "Lecture deleted",
        });
      });
  };

  const addItem = (variantIndex) => {
    const updatedVariants = [...variants];
    updatedVariants[variantIndex].items.push({
      title: "",
      description: "",
      file: "",
      preview: false,
    });

    setVariants(updatedVariants);
  };

  const removeItem = (variantIndex, itemIndex, variantId, itemId) => {
    const updatedVariants = [...variants];
    updatedVariants[variantIndex].items.splice(itemIndex, 1);
    setVariants(updatedVariants);

    useAxios()
      .delete(
        `teacher/course/variant-item-delete/${variantId}/${itemId}/${UserData()?.teacher_id}/${param.course_id}/`
      )
      .then((res) => {
        console.log(res.data);
        fetchCourseDetail();
        Toast().fire({
          icon: "success",
          title: "Lesson Item deleted",
        });
      });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formdata = new FormData();
    formdata.append("title", course.title);
    formdata.append("description", ckEdtitorData);
    formdata.append("category", course.category);
    formdata.append("price", course.price);
    formdata.append("level", course.level);
    formdata.append("language", course.language);
    formdata.append("teacher", parseInt(UserData()?.teacher_id));
    console.log(course.category);

    if (course.file !== null || course.file !== "") {
      formdata.append("file", course.file || "");
    }

    if (course.image.file) {
      formdata.append("image", course.image.file);
    }

    variants.forEach((variant, variantIndex) => {
      Object.entries(variant).forEach(([key, value]) => {
        console.log(`Key: ${key} = value: ${value}`);
        formdata.append(
          `variants[${variantIndex}][variant_${key}]`,
          String(value)
        );
      });

      variant.items.forEach((item, itemIndex) => {
        Object.entries(item).forEach(([itemKey, itemValue]) => {
          formdata.append(
            `variants[${variantIndex}][items][${itemIndex}][${itemKey}]`,
            itemValue
          );
        });
      });
    });

    const response = await useAxios().patch(
      `teacher/course-update/${UserData()?.teacher_id}/${param.course_id}/`,
      formdata
    );
    console.log(response.data);
    Swal.fire({
      icon: "success",
      title: "Course Updated Successfully",
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
            <form className="col-lg-9 col-md-8 col-12" onSubmit={handleSubmit}>
              <>
                <section className="py-4 py-lg-6 bg-primary rounded-3">
                  <div className="container">
                    <div className="row">
                      <div className="offset-lg-1 col-lg-10 col-md-12 col-12">
                        <div className="d-lg-flex align-items-center justify-content-between">
                          {/* Content */}
                          <div className="mb-4 mb-lg-0">
                            <h1 className="text-white mb-1">Add New Course</h1>
                            <p className="mb-0 text-white lead">
                              Just fill the form and create your courses.
                            </p>
                          </div>
                          <div>
                            <Link
                              to="/instructor/courses/"
                              className="btn"
                              style={{ backgroundColor: "white" }}
                            >
                              {" "}
                              <i className="fas fa-arrow-left"></i> Back to
                              Course
                            </Link>
                            <a
                              href="instructor-courses.html"
                              className="btn btn-dark ms-2"
                            >
                              Save <i className="fas fa-check-circle"></i>
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>
                <section className="pb-8 mt-5">
                  <div className="card mb-3">
                    {/* Basic Info Section */}
                    <div className="card-header border-bottom px-4 py-3">
                      <h4 className="mb-0">Basic Information</h4>
                    </div>
                    <div className="card-body">
                      <label htmlFor="courseTHumbnail" className="form-label">
                        Thumbnail Preview
                      </label>
                      <img
                        style={{
                          width: "100%",
                          height: "330px",
                          objectFit: "cover",
                          borderRadius: "10px",
                        }}
                        className="mb-4"
                        src={
                          course.image.preview ||
                          course.image ||
                          "https://www.eclosio.ong/wp-content/uploads/2018/08/default.png"
                        }
                        alt=""
                      />
                      <div className="mb-3">
                        <label htmlFor="courseTHumbnail" className="form-label">
                          Course Thumbnail
                        </label>
                        <input
                          id="courseTHumbnail"
                          className="form-control"
                          type="file"
                          name="image"
                          onChange={handleCourseImageChange}
                        />
                      </div>
                      <div className="mb-3">
                        <label htmlFor="courseTitle" className="form-label">
                          Intro Video
                        </label>
                        <input
                          id="introvideo"
                          className="form-control"
                          type="file"
                          name="file"
                          onChange={handleCourseIntroVideoChange}
                        />
                      </div>
                      <div className="mb-3">
                        <label htmlFor="courseTitle" className="form-label">
                          Title
                        </label>
                        <input
                          id="courseTitle"
                          className="form-control"
                          type="text"
                          placeholder=""
                          name="title"
                          defaultValue={course.title}
                          onChange={handleCourseInputChange}
                        />
                        <small>Write a 60 character course title.</small>
                      </div>
                      <div className="mb-3">
                        <label className="form-label">Courses category</label>
                        <select
                          className="form-select"
                          name="category"
                          onChange={handleCourseInputChange}
                          value={course.category.id}
                        >
                          <option value="">-------------</option>
                          {category?.map((c, index) => (
                            <option key={index} value={c.id}>
                              {c.title}
                            </option>
                          ))}
                        </select>
                        <small>
                          Help people find your courses by choosing categories
                          that represent your course.
                        </small>
                      </div>
                      <div className="mb-3">
                        <select
                          className="form-select"
                          onChange={handleCourseInputChange}
                          name="level"
                          value={course.level}
                        >
                          <option value="">Select level</option>
                          <option value="Beginner">Beginner</option>
                          <option value="Intemediate">Intemediate</option>
                          <option value="Advanced">Advanced</option>
                        </select>
                      </div>

                      <div className="mb-3">
                        <select
                          className="form-select"
                          onChange={handleCourseInputChange}
                          name="language"
                          value={course.language}
                        >
                          <option value="">Select Language</option>
                          <option value="English">English</option>
                          <option value="Spanish">Spanish</option>
                          <option value="French">French</option>
                        </select>
                      </div>
                      <div className="mb-3">
                        <label className="form-label">Course Description</label>
                        <CKEditor
                          editor={ClassicEditor}
                          data={ckEdtitorData}
                          onChange={handleCkEditorChange}
                          style={{ height: "400px" }}
                          name="description"
                          value={course.description || ""}
                        />
                        <small>A brief summary of your courses.</small>
                      </div>
                      <label htmlFor="courseTitle" className="form-label">
                        Price
                      </label>
                      <input
                        id="courseTitle"
                        className="form-control"
                        type="number"
                        onChange={handleCourseInputChange}
                        name="price"
                        placeholder="$20.99"
                      />
                    </div>

                    {/* Curriculum Section */}
                    <div className="card-header border-bottom px-4 py-3">
                      <h4 className="mb-0">Curriculum</h4>
                    </div>
                    <div className="card-body ">
                      {variants?.map((variant, variantIndex) => (
                        <div
                          className="border p-2 rounded-3 mb-3"
                          style={{ backgroundColor: "#ededed" }}
                        >
                          <div className="d-flex mb-4">
                            <input
                              type="text"
                              placeholder="Section Name"
                              required
                              value={variant.title}
                              className="form-control"
                              onChange={(e) =>
                                handleVariantChange(
                                  variantIndex,
                                  "title",
                                  e.target.value
                                )
                              }
                            />
                            <button
                              className="btn btn-danger ms-2"
                              type="button"
                              onClick={() =>
                                removeVariant(variantIndex, variant.id)
                              }
                            >
                              <i className="fas fa-trash"></i>
                            </button>
                          </div>
                          {variant?.items?.map((item, itemIndex) => (
                            <div
                              className=" mb-2 mt-2 shadow p-2 rounded-3 "
                              style={{ border: "1px #bdbdbd solid" }}
                            >
                              <input
                                type="text"
                                placeholder="Lesson Title"
                                className="form-control me-1 mt-2"
                                name="title"
                                value={item.title}
                                onChange={(e) =>
                                  handleItemChange(
                                    variantIndex,
                                    itemIndex,
                                    "title",
                                    e.target.value,
                                    e.target.type
                                  )
                                }
                              />
                              <textarea
                                name="description"
                                id=""
                                value={item.description}
                                cols="30"
                                className="form-control mt-2"
                                placeholder="Lesson Description"
                                rows="4"
                                onChange={(e) =>
                                  handleItemChange(
                                    variantIndex,
                                    itemIndex,
                                    "description",
                                    e.target.value,
                                    e.target.type
                                  )
                                }
                              ></textarea>
                              <div className="row d-flex align-items-center">
                                <div className="col-lg-8">
                                  <input
                                    type="file"
                                    placeholder="Item Price"
                                    className="form-control me-1 mt-2"
                                    name="file"
                                    onChange={(e) =>
                                      handleItemChange(
                                        variantIndex,
                                        itemIndex,
                                        "file",
                                        e.target.files[0],
                                        e.target.type
                                      )
                                    }
                                  />
                                </div>
                                <div className="col-lg-4">
                                  <label htmlFor={`checkbox${1}`}>
                                    Preview
                                  </label>
                                  <input
                                    type="checkbox"
                                    className="form-check-input ms-2"
                                    name=""
                                    checked={item.preview}
                                    id={`checkbox${1}`}
                                    onChange={(e) =>
                                      handleItemChange(
                                        variantIndex,
                                        itemIndex,
                                        "preview",
                                        e.target.checked,
                                        e.target.type
                                      )
                                    }
                                  />
                                </div>
                              </div>
                              <button
                                className="btn btn-sm btn-outline-danger me-2 mt-2"
                                type="button"
                                onClick={() =>
                                  removeItem(
                                    variantIndex,
                                    itemIndex,
                                    variant.variant_id,
                                    item.variant_item_id
                                  )
                                }
                              >
                                Delete Lesson <i className="fas fa-trash"></i>
                              </button>
                            </div>
                          ))}

                          <button
                            className="btn btn-sm btn-primary mt-2"
                            type="button"
                            onClick={() => addItem(variantIndex)}
                          >
                            + Add Lesson
                          </button>
                        </div>
                      ))}

                      <button
                        className="btn btn-sm btn-secondary w-100 mt-2"
                        type="button"
                        onClick={addVariant}
                      >
                        + New Section
                      </button>
                    </div>
                  </div>
                  <button
                    className="btn btn-lg btn-success w-100 mt-2"
                    type="submit"
                  >
                    Create Course <i className="fas fa-check-circle"></i>
                  </button>
                </section>
              </>
            </form>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default CourseEdit;
