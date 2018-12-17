/*
 * This file is part of the PSL software.
 * Copyright 2011-2015 University of Maryland
 * Copyright 2013-2015 The Regents of the University of California
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package edu.umd.cs.psl.database;

import java.util.Set;

import edu.umd.cs.psl.database.loading.Inserter;
import edu.umd.cs.psl.database.loading.Updater;
import edu.umd.cs.psl.model.argument.UniqueID;
import edu.umd.cs.psl.model.atom.GroundAtom;
import edu.umd.cs.psl.model.predicate.StandardPredicate;

/**
 * Makes {@link GroundAtom GroundAtoms} available via {@link Database Databases}.
 * <p>
 * GroundAtoms with {@link StandardPredicate StandardPredicates} can be persisted
 * in a DataStore's {@link Partition Partitions}. If a StandardPredicate has not
 * been persisted before in a DataStore, it must be registered via
 * {@link #registerPredicate(StandardPredicate)}.
 */
public interface DataStore {

	/**
	 * Registers a StandardPredicate so that {@link GroundAtom GroundAtoms} of that
	 * StandardPredicate can be persisted in this DataStore.
	 * <p>
	 * If GroundAtoms of a StandardPredicate were already persisted in this DataStore
	 * at initialization, that StandardPredicate is already registered.
	 * 
	 * @param predicate  the predicate to register
	 */
	public void registerPredicate(StandardPredicate predicate);
	
	/**
	 * Creates a Database that can read from and write to a {@link Partition} and
	 * optionally read from additional Partitions.
	 * 
	 * @param write  the Partition to write to and read from
	 * @param read  additional Partitions to read from
	 * @return a new Database backed by this DataStore
	 * @throws IllegalArgumentException  if write is in use or if read is the
	 *                                       write Partition of another Database
	 */
	public Database getDatabase(Partition write, Partition... read);
	
	/**
	 * Creates a Database that can read from and write to a {@link Partition} and
	 * optionally read from additional Partitions.
	 * <p>
	 * Additionally, defines a set of StandardPredicates as closed in the Database,
	 * meaning that all GroundAtoms of that Predicate are ObservedAtoms.
	 * 
	 * @param write  the Partition to write to and read from
	 * @param toClose  set of StandardPredicates to close
	 * @param read  additional Partitions to read from
	 * @return a new Database backed by this DataStore
	 * @throws IllegalArgumentException  if write is in use or if read is the
	 *                                       write Partition of another Database
	 */
	public Database getDatabase(Partition write, Set<StandardPredicate> toClose, Partition... read);
	
	/**
	 * Returns a UniqueID based on the given key.
	 * <p>
	 * An Integer must always be a valid key. Other types may be supported by
	 * implementations and/or configurations.
	 * <p>
	 * If two keys are equal, they must map to the same UniqueID.
	 * 
	 * @param key  the key to a UniqueID
	 * @return the UniqueID indicated by key
	 * @throws IllegalArgumentException  if the key is invalid
	 */
	public UniqueID getUniqueID(Object key);
	
	/**
	 * Creates an Inserter for persisting new {@link GroundAtom GroundAtoms}
	 * in a {@link Partition}.
	 * 
	 * @param predicate  the Predicate of the Atoms to be inserted
	 * @param partition  the Partition into which Atoms will be inserted
	 * @return the Inserter
	 * @throws IllegalArgumentException  if partition is in use or predicate is
	 *                                       not registered
	 */
	public Inserter getInserter(StandardPredicate predicate, Partition partition);
	
	/**
	 * Creates an Updater for updating {@link GroundAtom GroundAtoms} persisted
	 * in a {@link Partition}.
	 * 
	 * @param predicate  the Predicate of the Atoms to be updated
	 * @param partition  the Partition of the Atoms to be updated
	 * @return the Updater
	 * @throws IllegalArgumentException  if partition is in use or predicate is
	 *                                       not registered
	 */
	public Updater getUpdater(StandardPredicate predicate, Partition partition);
	
	/**
	 * Returns the set of StandardPredicates registered with this DataStore.
	 * Note that the result can differ from calling
	 * {@link Database#getRegisteredPredicates()} on an associated Database,
	 * since additional predicates might have been registered since that Database
	 * was created.
	 * 
	 * @return the set of StandardPredicates registered with this DataStore
	 */
	public Set<StandardPredicate> getRegisteredPredicates();
	
	/**
	 * Deletes all {@link GroundAtom GroundAtoms} persisted in a Partition.
	 *  
	 * @param partition  the partition to delete
	 * @return the number of Atoms deleted
	 * @throws IllegalArgumentException  if partition is in use
	 */
	public int deletePartition(Partition partition);
	
	/**
	 * Releases all resources and locks obtained by this DataStore.
	 * 
	 * @throws IllegalStateException  if any Partitions are in use
	 */
	public void close();

	/**
	 * Get the next available partition 
	 * 
	 * @return the next available partition 
	 */
	Partition getNextPartition();
	
}
