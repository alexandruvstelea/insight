from flask import Blueprint, jsonify, request, abort
from models.subjectLike import SubjectLike
from __init__ import db, limiter
from sqlalchemy import exc
from bleach import clean
from flask_jwt_extended import jwt_required
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)
subjectLike_bp = Blueprint("subjectLike", __name__)


@subjectLike_bp.route("/likes/<int:subject_id>", methods=["POST"])
# @jwt_required()
@limiter.limit("50 per minute")
def add_subject_like(subject_id):
    ip_address = request.remote_addr
    try:
        like_dislike = request.json.get("like_dislike", True)
        existing_vote = (
            db.session.query(SubjectLike)
            .filter_by(subject_id=subject_id, ip_address=ip_address)
            .first()
        )

        if existing_vote:
            # Actualizare vot existent
            existing_vote.like_dislike = like_dislike
            logger.info(f"Updated vote for IP {ip_address} on subject {subject_id}")
        else:
            # Adăugare vot nou
            new_like = SubjectLike(
                subject_id=subject_id, ip_address=ip_address, like_dislike=like_dislike
            )
            db.session.add(new_like)
            logger.info(f"Added new vote for IP {ip_address} on subject {subject_id}")

        db.session.commit()
        return jsonify({"response": "Vote recorded"}), 200

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"An error occurred while recording the vote.\n {e}")
        abort(500, "Error recording the vote.")


@subjectLike_bp.route("/likes/<int:subject_id>", methods=["GET"])
@limiter.limit("50 per minute")
def get_subject_likes(subject_id):
    try:
        likes_count = (
            db.session.query(func.count(SubjectLike.id))
            .filter_by(subject_id=subject_id, like_dislike=True)
            .scalar()
        )
        dislikes_count = (
            db.session.query(func.count(SubjectLike.id))
            .filter_by(subject_id=subject_id, like_dislike=False)
            .scalar()
        )

        return jsonify({"likes": likes_count, "dislikes": dislikes_count}), 200
    except exc.SQLAlchemyError as e:
        logger.error(f"An error occurred while retrieving likes/dislikes.\n {e}")
        abort(500, "Error retrieving likes/dislikes.")


@subjectLike_bp.route("/likes/dev/<int:subject_id>", methods=["POST"])
@limiter.limit("50 per minute")
def add_subject_like_dev(subject_id):
    try:
        like_dislike = request.json.get("like_dislike", True)

        new_like = SubjectLike(
            subject_id=subject_id, ip_address="dev-ip", like_dislike=like_dislike
        )
        db.session.add(new_like)

        logger.info(f"Added new vote for development on subject {subject_id}")

        db.session.commit()
        return jsonify({"response": "Vote recorded"}), 200

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"An error occurred while recording the vote.\n {e}")
        abort(500, "Error recording the vote.")
