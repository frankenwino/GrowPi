import datetime


def get_utc_datetime():
    # Get the current UTC time
    utc_time = datetime.datetime.utcnow()

    # Return the time in ISO 8601 format (without microseconds)
    return utc_time.replace(microsecond=0).isoformat()


# Example usage
if __name__ == "__main__":
    print("Current UTC Date and Time:", get_utc_datetime())
