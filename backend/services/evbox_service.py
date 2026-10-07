from database import Database
from services.user_service import get_user_role_from_db

def get_all_evboxes():
    try:
        with Database() as DB:
            query = """
            SELECT 
                EVBoxes.*, 
                EVBOXLocations.locationName,
                CASE 
                    WHEN EXISTS (
                        SELECT 1 
                        FROM chargeSessions cs 
                        WHERE cs.EVBOXID = EVBoxes.EVBOXID 
                        AND cs.sessionEnd IS NULL 
                        AND cs.status = 'active'
                    ) THEN TRUE 
                    ELSE FALSE 
                END AS isUsed,
                (
                    SELECT DATE_FORMAT(MAX(sessionEnd), '%d-%m-%Y') 
                    FROM chargeSessions cs 
                    WHERE cs.EVBOXID = EVBoxes.EVBOXID 
                    AND cs.status = 'completed'
                ) AS laatste_sessie_datum,
                COALESCE(
                    (
                        SELECT SUM(energyUsage) 
                        FROM chargeSessions cs 
                        WHERE cs.EVBOXID = EVBoxes.EVBOXID 
                        AND cs.status = 'completed'
                    ), 0
                ) AS total_energy
            FROM EVBoxes 
            INNER JOIN EVBOXLocations 
                ON EVBoxes.locationID = EVBOXLocations.locationID
            ORDER BY EVBoxes.EVBOXID;
            """
            DB.execute_query(query)
            return DB.fetch_results()
    except Exception as e:
        print(f"Error in get_all_evboxes: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van de laadpalen"}

def get_active_session(evbox_id):
    try:
        with Database() as DB:
            query = """
            SELECT 
                cs.sessionID,
                cs.sessionStart,
                cs.energyUsage,
                cs.totalCost,
                CONCAT(u.firstName, ' ', u.nameParticle, ' ', u.lastName) AS userName,
                u.email,
                TIMESTAMPDIFF(MINUTE, cs.sessionStart, NOW()) AS durationMinutes
            FROM chargeSessions cs
            INNER JOIN userCards uc ON cs.cardUID = uc.cardUID
            INNER JOIN users u ON uc.userID = u.userID
            WHERE cs.EVBOXID = %s 
            AND cs.sessionEnd IS NULL 
            AND cs.status = 'active'
            LIMIT 1;
            """
            DB.execute_query(query, (evbox_id,))
            result = DB.fetch_results()
            return result[0] if result else {"message": "Geen actieve sessie"}
    except Exception as e:
        print(f"Error in get_active_session: {e}")
        return {"error": "Er is een fout opgetreden"}

def get_session_history(evbox_id):
    try:
        with Database() as DB:
            query = """
            SELECT 
                cs.sessionID,
                cs.sessionStart,
                cs.sessionEnd,
                cs.energyUsage,
                cs.totalCost,
                cs.status,
                CONCAT(u.firstName, ' ', 
                    CASE 
                        WHEN u.nameParticle != '' THEN CONCAT(u.nameParticle, ' ')
                        ELSE ''
                    END,
                    u.lastName) AS userName,
                u.email,
                TIMESTAMPDIFF(MINUTE, cs.sessionStart, cs.sessionEnd) AS durationMinutes
            FROM chargeSessions cs
            INNER JOIN userCards uc ON cs.cardUID = uc.cardUID
            INNER JOIN users u ON uc.userID = u.userID
            WHERE cs.EVBOXID = %s 
            AND cs.status = 'completed'
            ORDER BY cs.sessionEnd DESC
            LIMIT 50;
            """
            DB.execute_query(query, (evbox_id,))
            return DB.fetch_results()
    except Exception as e:
        print(f"Error in get_session_history: {e}")
        return {"error": "Er is een fout opgetreden"}

def get_all_session_history(limit=500):
    try:
        with Database() as DB:
            query = """
            SELECT 
                cs.sessionID,
                cs.EVBOXID,
                cs.sessionStart,
                cs.sessionEnd,
                cs.energyUsage,
                cs.totalCost,
                cs.status,
                CONCAT(u.firstName, ' ', 
                    CASE 
                        WHEN u.nameParticle != '' THEN CONCAT(u.nameParticle, ' ')
                        ELSE ''
                    END,
                    u.lastName) AS userName,
                u.email,
                TIMESTAMPDIFF(MINUTE, cs.sessionStart, cs.sessionEnd) AS durationMinutes
            FROM chargeSessions cs
            INNER JOIN userCards uc ON cs.cardUID = uc.cardUID
            INNER JOIN users u ON uc.userID = u.userID
            WHERE cs.status = 'completed'
            ORDER BY cs.sessionEnd DESC
            LIMIT %s;
            """
            DB.execute_query(query, (limit,))
            return DB.fetch_results()
    except Exception as e:
        print(f"Error in get_all_session_history: {e}")
        return {"error": "Er is een fout opgetreden"}

def get_all_sessions(user_id,start_date=None, end_date=None, limit=500):
    try:
        with Database() as DB:
            query = """
            SELECT 
                cs.sessionID,
                cs.EVBOXID,
                cs.locationName,
                cs.sessionStart,
                cs.sessionEnd,
                cs.energyUsage,
                cs.totalCost,
                cs.status,
                CONCAT(u.firstName, ' ', 
                    CASE 
                        WHEN u.nameParticle != '' THEN CONCAT(u.nameParticle, ' ')
                        ELSE ''
                    END,
                    u.lastName) AS userName,
                u.email,
                TIMESTAMPDIFF(MINUTE, cs.sessionStart, cs.sessionEnd) AS durationMinutes
            FROM chargeSessions cs
            INNER JOIN userCards uc ON cs.cardUID = uc.cardUID
            INNER JOIN users u ON uc.userID = u.userID """

            if get_user_role_from_db(user_id)[0].get("role") != "admin":
                query += """WHERE u.userID = %s """

            if start_date and end_date:
                query += """WHERE DATE(cs.sessionStart) BETWEEN %s AND %s"""

            query += """ORDER BY cs.sessionID DESC
            LIMIT %s;
            """

            if get_user_role_from_db(user_id)[0].get("role") != "admin":
                if start_date and end_date:
                    DB.execute_query(query, (user_id, start_date, end_date, limit))
                else:
                    DB.execute_query(query, (user_id, limit))

            elif start_date and end_date:
                DB.execute_query(query, (start_date, end_date, limit))
            else:
                DB.execute_query(query, (limit,))

            return DB.fetch_results()
    except Exception as e:
        print(f"Error in get_all_session_history: {e}")
        return {"error": "Er is een fout opgetreden"}

def get_evbox_info(evbox_id):
    try:
        with Database() as DB:
            query = """
            SELECT 
                EVBoxes.EVBOXID,
                EVBoxes.softwareVersion,
                EVBoxes.status,
                EVBOXLocations.locationName,
                EVBOXLocations.address,
                EVBOXLocations.city
            FROM EVBoxes 
            INNER JOIN EVBOXLocations 
                ON EVBoxes.locationID = EVBOXLocations.locationID
            WHERE EVBoxes.EVBOXID = %s;
            """
            DB.execute_query(query, (evbox_id,))
            result = DB.fetch_results()
            return result[0] if result else {"error": "Laadpaal niet gevonden"}
    except Exception as e:
        print(f"Error in get_evbox_info: {e}")
        return {"error": "Er is een fout opgetreden"}
    
def get_total_energy(start_date, end_date):
    """Get total energy usage in kWh for a date range"""
    try:
        with Database() as DB:
            query = """
            SELECT
                COALESCE(SUM(energyUsage), 0) AS totalEnergy
            FROM chargeSessions
            WHERE status = 'completed'
            AND DATE(sessionEnd) BETWEEN %s AND %s;
            """
            DB.execute_query(query, (start_date, end_date))
            result = DB.fetch_one()
            return result if result else {"totalEnergy": 0}
    except Exception as e:
        print(f"Error in get_total_energy: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van de totale energieverbruik"}
    
def get_total_cost(start_date, end_date):
    """Get total cost for a date range"""
    try:
        with Database() as DB:
            query = """
            SELECT
                COALESCE(SUM(totalCost), 0) AS totalCost
            FROM chargeSessions
            WHERE status = 'completed'
            AND DATE(sessionEnd) BETWEEN %s AND %s;
            """
            DB.execute_query(query, (start_date, end_date))
            result = DB.fetch_one()
            return result if result else {"totalCost": 0}
    except Exception as e:
        print(f"Error in get_total_cost: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van de totale kosten"}

def get_total_sessions(start_date, end_date):
    """Get total number of completed sessions for a date range"""
    try:
        with Database() as DB:
            query = """
            SELECT 
                COUNT(*) AS totalSessions
            FROM chargeSessions
            WHERE status = 'completed'
            AND DATE(sessionStart) BETWEEN %s AND %s;
            """
            DB.execute_query(query, (start_date, end_date))
            result = DB.fetch_one()

            print(f"Total sessions from {start_date} to {end_date}: {result}")

            return result if result else {"totalSessions": 0}
    except Exception as e:
        print(f"Error in get_total_sessions: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van sessies"}

def get_active_chargers():
    """Get number of currently active chargers"""
    try:
        with Database() as DB:
            query = """
            SELECT
                COUNT(DISTINCT EVBOXID) AS activeChargers
            FROM chargeSessions
            WHERE status = 'active'
            AND sessionEnd IS NULL;
            """
            DB.execute_query(query)
            result = DB.fetch_one()
            return result if result else {"activeChargers": 0}
    except Exception as e:
        print(f"Error in get_active_chargers: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van de actieve laadpalen"}
    
def get_dashboard_metrics(start_date, end_date):
    """Get all dashboard metrics (total energy, sessions, active chargers)"""
    try:
        total_energy = get_total_energy(start_date, end_date)
        total_sessions = get_total_sessions(start_date, end_date)
        total_cost = get_total_cost(start_date, end_date)
        active_chargers = get_active_chargers()
        session_history = get_all_session_history(500)
        
        # Check for errors in any of the results
        if "error" in total_energy or "error" in total_sessions or "error" in active_chargers:
            return {"error": "Er is een fout opgetreden bij het ophalen van dashboard gegevens"}
        
        return {
            "totalEnergy": total_energy.get("totalEnergy", 0),
            "totalSessions": total_sessions.get("totalSessions", 0),
            "totalCost": total_cost.get("totalCost", 0),
            "activeChargers": active_chargers.get("activeChargers", 0),
            "period": {
                "startDate": start_date,
                "endDate": end_date
            }
        }
    except Exception as e:
        print(f"Error in get_dashboard_metrics: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van dashboard gegevens"}

def get_all_locations():
    try:
        with Database() as DB:
            query = """
            SELECT 
                locationID,
                locationName,
                address,
                city
            FROM EVBOXLocations
            ORDER BY locationID;
            """
            DB.execute_query(query)
            return DB.fetch_results()
    except Exception as e:
        print(f"Error in get_all_locations: {e}")
        return {"error": "Er is een fout opgetreden bij het ophalen van de locaties"}