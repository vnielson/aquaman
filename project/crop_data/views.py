from flask import render_template, Blueprint, url_for, redirect, jsonify, request
from project import db
from project.models import Crops
from project.crop_data.forms import AddCropForm, DeleteCropForm

crop_data = Blueprint('crop_data', __name__)


def load_data():

    crop_data = []
    crops = Crops.query.all()
    for s in crops:
        next_crop = s.__dict__
        del next_crop["_sa_instance_state"]
        crop_data.append(next_crop)

    print("Crop Data... ")
    print(crop_data)
    return crop_data

@crop_data.route('/crops/', methods=['GET'])
def get_data():
    print("IN getData for crops")
    return jsonify(load_data())


@crop_data.route('/crops/', methods=['POST',])
def insert_data():
    print("Insert Crop Request...")
    new_crop_data = request.json
    print(new_crop_data)

    # Create the New Crop

    new_crop = Crops(
        crop_name=new_crop_data["crop_name"],
        ideal_kpa=new_crop_data["ideal_kpa"],
        dry_kpa=new_crop_data["dry_kpa"],
        saturated_kpa=new_crop_data["saturated_kpa"]
        )




    db.session.add(new_crop)
    db.session.commit()



    ret_crop = {
        "crop_id": new_crop.crop_id,
        "crop_name": new_crop.crop_name,
        "ideal_kpa": new_crop.ideal_kpa,
        "dry_kpa": new_crop.dry_kpa,
        "saturated_kpa": new_crop.saturated_kpa
    }

    return jsonify(ret_crop)
    # return jsonify(success=True)




@crop_data.route('/crops/<int:crop_id>', methods=['PUT',])
def update_crop(crop_id):

    print("UPDATE VALVE:")
    #Find item to update
    jsonrequest = request.json
    print("json request")
    print(jsonrequest)

    crop = db.session.query(Crops).get(jsonrequest["crop_id"]);
    print("Crop to be updated:")
    print(crop)

    update = {
        "crop_name" : jsonrequest["crop_name"],
        "ideal_kpa" : jsonrequest["ideal_kpa"],
        "dry_kpa": jsonrequest["dry_kpa"],
        "saturated_kpa": jsonrequest["saturated_kpa"]
    }


    print(update)

    db.session.query(Crops).filter_by(crop_id=jsonrequest["crop_id"]).update(update)
    db.session.commit();


    return jsonify(request.json)
    # return jsonify(success=True)


@crop_data.route('/crops/<int:crop_id>', methods=['DELETE',])
def delete_crop(crop_id):

    crop = db.session.query(Crops).get(crop_id);

    del_crop_return = db.session.delete(crop)
    print("Return value  ", del_crop_return)

    db.session.commit()

    return jsonify(success=True)


