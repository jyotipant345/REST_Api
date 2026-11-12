
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample student records
students = [
    {"id": 1, "name": "Jyoti Pant", "branch": "MCA", "cgpa": 8.5},
    {"id": 2, "name": "Nidhi Mishra", "branch": "MCA", "cgpa": 9.0}
]

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Student REST API",
        "status": "API is running successfully"
    })

# GET: Retrieve all students
@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(students), 200

# GET: Retrieve one student by ID
@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student), 200

    return jsonify({"error": "Student not found"}), 404

# POST: Add a new student
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    if not all(key in data for key in ["name", "branch", "cgpa"]):
        return jsonify({"error": "Name, branch and CGPA are required"}), 400

    try:
        cgpa = float(data["cgpa"])
    except (ValueError, TypeError):
        return jsonify({"error": "CGPA must be a number"}), 400

    if not 0 <= cgpa <= 10:
        return jsonify({"error": "CGPA must be between 0 and 10"}), 400

    new_id = max([s["id"] for s in students], default=0) + 1

    new_student = {
        "id": new_id,
        "name": str(data["name"]),
        "branch": str(data["branch"]),
        "cgpa": cgpa
    }

    students.append(new_student)

    return jsonify({
        "message": "Student added successfully",
        "student": new_student
    }), 201

# PUT: Update an existing student
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}

    for student in students:
        if student["id"] == student_id:
            if "name" in data:
                student["name"] = str(data["name"])
            if "branch" in data:
                student["branch"] = str(data["branch"])
            if "cgpa" in data:
                try:
                    cgpa = float(data["cgpa"])
                except (ValueError, TypeError):
                    return jsonify({"error": "CGPA must be a number"}), 400

                if not 0 <= cgpa <= 10:
                    return jsonify({"error": "CGPA must be between 0 and 10"}), 400

                student["cgpa"] = cgpa

            return jsonify({
                "message": "Student updated successfully",
                "student": student
            }), 200

    return jsonify({"error": "Student not found"}), 404

# DELETE: Delete a student
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message": "Student deleted successfully"}), 200

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
