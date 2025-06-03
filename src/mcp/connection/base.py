from abc import ABC,abstractmethod
from typing import Optional,Callable
import asyncio

class BaseConnection:
    def __init__(self):
        self.ready_event=asyncio.Event()
        self.done_event=asyncio.Event()
        self.exception:Optional[Exception]=None
        self.connection:Callable=None
        self.task:Optional[asyncio.Task]=None

    @abstractmethod
    async def establish_connection(self):
        '''
        Establish the connection

        This method should establish a specific type of connection.

        Returns:
            The connection
        Raises:
            Exception: If the connection could not be established
        '''
        pass

    @abstractmethod
    async def close_connection(self):
        '''
        Close the connection

        This method should close the specific type of connection
        '''
        pass

    async def start(self):
        '''
        Start the connection task

        Returns:
            The established connection

        Raises:
            Exception: If the connection could not be established
        '''
        # Reset the state
        self.ready_event.clear()
        self.done_event.clear()
        self.exception=None
        
        # Create a task to keep the connection alive
        self.task=asyncio.create_task(self.connection_task(),name='Connection Task')
        
        # Wait for the connection to be ready
        await self.ready_event.wait()

        # If there is an exception, raise it, otherwise return the connection
        if self.exception:
            raise self.exception
        if self.connection is None:
            raise RuntimeError('Connection could not be established')
        return self.connection

    async def stop(self):
        if self.task and not self.task.done():
            # Cancel the task
            self.task.cancel()
            # Wait for the task to stop
            try:
                await self.task
            except asyncio.CancelledError:
                # Expected behavior
                pass
            except Exception as e:
                print(f'Error while stopping the connection: {e}')

        # Wait for the connection to be done
        await self.done_event.wait()

    async def connection_task(self)->None:
        '''
        Keeps the connection alive by keeping the connection in background
        '''        
        try:
            # Establish the connection
            self.connection=await self.establish_connection()
            # Signal that the connection is ready
            self.ready_event.set()
            # Wait indefinitely until the connection is cancelled
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                # Expected behavior
                pass
        except Exception as e:
            #  Catch the exception
            self.exception=e
            # Signal that the connection ready (with error)
            self.ready_event.set()
        finally:
            # Close the connection
            if self.connection is not None:
                try:
                    await self.close_connection()
                except Exception as e:
                    self.connection=None
            # Signal that the connection is done
            self.done_event.set()
