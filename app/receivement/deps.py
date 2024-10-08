from fastapi import Depends
from app.common.dependencies import get_session
from app.receivement.services.lotting import LottingService
from app.receivement.services.receivement import ReceivementService
from sqlalchemy.orm import Session


def get_receivement_service(session: Session = Depends(get_session)):
    return ReceivementService(db=session)


def get_lotting_service(session: Session = Depends(get_session)):
    return LottingService(db=session)
